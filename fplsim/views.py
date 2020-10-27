from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import SquadPicker
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Player, Matchweek, Tweet, Result
import fplsim.tweet_scraper as twitter
import fplsim.sentiment_analysis as sentiment
from itertools import chain

scores = []


def squad_pick(request):
    if request.method == 'POST':
        form = SquadPicker(request.POST)
        if form.is_valid():
            # process data
            Goalkeeper = form.cleaned_data['GK']
            Defenders = form.cleaned_data['DEF']
            Midfielders = form.cleaned_data['MID']
            Forwards = form.cleaned_data['FWD']
            scraping_lvl = form.cleaned_data['choice']
            if len(Defenders) != 4:
                error3 = 'Four defenders required. Currently selected: {0}'.format(len(Defenders))
                messages.error(request, error3)
                return render_to_string('fplsim/selection.html', {'form': form,
                                                                  }, request)
            if len(Midfielders) != 4:
                error2 = 'Four midfielders required: use CTRL+Left (Windows) or CMD+Left (Mac) to select ' \
                         'multiple items. Currently selected: {0}'.format(len(Midfielders))
                messages.error(request, error2)
                return render_to_string('fplsim/selection.html', {'form': form,
                                                                  }, request)
            if len(Forwards) != 2:
                error1 = 'Two strikers required: use CTRL+Left (Windows) or CMD+Left (Mac) to select multiple items.' \
                         'Currently selected: {0}'.format(len(Forwards))
                messages.error(request, error1)
                return render_to_string('fplsim/selection.html', {'form': form,
                                                                  }, request)

            squad = list(chain([Goalkeeper], Defenders, Midfielders, Forwards))

            team_cost_ctrl = 0
            for player in squad:
                team_cost_ctrl += player.value
            budget = 5
            team_cost = team_cost_ctrl + budget

            total_points = 0
            points_ctrl = []
            total_points_ctrl = 0
            matchcount = 1
            matchcount_ctrl = 1
            results = []

            # calculate total points without swaps (control)
            while matchcount_ctrl < 6:
                week_total = 0
                for player in squad:
                    match = Matchweek.objects.filter(player=player, round=matchcount_ctrl)
                    if match:
                        week_total += match[0].total_points
                points_ctrl.append(week_total)
                matchcount_ctrl += 1
            total_points_ctrl = sum(points_ctrl)

            # call simulation for 5 rounds with squad
            while matchcount < 6:
                points, squad, budget, result_dict, tweet_url = simulation(squad, budget,
                                                                           int(scraping_lvl), matchcount)
                matchcount += 1
                total_points += points
                results.append((result_dict, points_ctrl[matchcount - 2], tweet_url))

            team_cost -= budget

            allData = Result.objects.all()
            dataPoint_ctrl = Result(points=total_points_ctrl, cost=round(team_cost_ctrl, 2),
                                    scraping_level=-1)
            # only save if data point does not exist:
            if len(Result.objects.filter(points=total_points_ctrl, cost=round(team_cost_ctrl, 2),
                                         scraping_level=-1)) == 0:
                dataPoint_ctrl.save()
            dataPoint = Result(points=total_points, cost=round(team_cost, 2),
                               scraping_level=int(scraping_lvl))
            # only save if data point does not exist:
            if len(Result.objects.filter(points=total_points, cost=round(team_cost, 2),
                                         scraping_level=int(scraping_lvl))) == 0:
                dataPoint.save()
            histogramData = []
            scatterplot_sent = []
            scatterplot_form = []
            scatterplot_ctrl = []
            for data in allData:
                histogramData.append(round(data.points / data.cost, 2))
                if data.scraping_level == 0:
                    scatterplot_form.append([data.cost, data.points])
                elif data.scraping_level == 1:
                    scatterplot_sent.append([data.cost, data.points])
                elif data.scraping_level == -1:
                    scatterplot_ctrl.append([data.cost, data.points])

            context = {'total_points': [total_points],
                       'total_points_ctrl': total_points_ctrl,
                       'squad': squad,
                       'results': results,
                       'dataPoint_h': [[len(histogramData),
                                        round(dataPoint.points / dataPoint.cost, 2)]],
                       'dataPoint_s': [[dataPoint.cost, dataPoint.points]],
                       'histogramData': histogramData,
                       'team_cost': [round(team_cost, 2), round(team_cost_ctrl, 2)],
                       'scatterplot_ctrl': scatterplot_ctrl,
                       'scatterplot_sent': scatterplot_sent,
                       'scatterplot_form': scatterplot_form,
                       'sentiment_level': int(scraping_lvl),
                       }

            return render_to_string('fplsim/results.html', context, request)
    else:
        form = SquadPicker()
    return render_to_string('fplsim/selection.html', {'form': form,
                                                      }, request)


def simulation(squad, budget, scraping_level, matchcount):
    # helper function to swap one player for another in the same position
    def replace(player, budget, squad):
        replacement = None
        position = player.position

        suitors = Player.objects.filter(position=position,
                                        value__lte=budget,
                                        matchweek__round=matchcount
                                        ).order_by('matchweek__total_points')
        for suitor in suitors:

            if suitor not in squad:
                replacement = suitor
        if not replacement:
            return replacement, budget
        else:
            budget -= replacement.value
            return replacement, budget

    # date strings of matches in 2017 for api.search function
    dates = ['2017-08-13', '2017-08-19', '2017-08-26', '2017-09-11', '2017-09-16',
             '2017-09-23', '2017-09-30', '2017-10-14', '2017-10-20', '2017-10-28',
             '2017-11-04', '2017-11-19', '2017-11-24', '2017-11-29', '2017-12-03',
             '2017-12-09', '2017-12-13', '2017-12-16', '2017-12-23', '2017-12-31']
    result_dict = {}
    result_list = ""
    swap = ""

    # for every matchweek calculate total points
    pointsList = []
    for player in squad:
        match = Matchweek.objects.filter(player=player, round=matchcount)
        if match:
            pointsList.append(match[0].total_points)

    points = sum(pointsList)
    # find lowest performers based on performance
    worstPlayers = []
    worstData = []

    if scraping_level == 0:
        minVal = min(pointsList)
        minIndex = pointsList.index(minVal)
        worstPlayers.append((squad[minIndex], minIndex))
        worstData.append(pointsList[minVal])

    # find lowest performers based on scraped data
    headlines = []
    sentimentList = []
    tweet_urls = []
    tweet_url = None
    if scraping_level == 1:
        for player in squad:
            tweet = Tweet.objects.filter(player=player, round=matchcount)
            if tweet:
                headlines.append(tweet[0].text)
                sentimentList.append(tweet[0].sentiment)
                tweet_urls.append(tweet[0].url)
            else:
                tweet_urls.append('')
                headlines.append([''])
                sentimentList.append(2)
        minVal = min(sentimentList)
        if minVal < 0:
            minIndex = sentimentList.index(minVal)
            worstData.append(sentimentList[minIndex])
            worstPlayers.append((squad[minIndex], minIndex))
            tweet_url = tweet_urls[minIndex]
        else:
            swap = "None"
            result_list = "No tweets with negative sentiment found for any player."

    # calculate budget for swap
    for player, _ in worstPlayers:
        budget += player.value

    if worstPlayers:
        # swap worst players (the replacement cannot already be in the squad)
        player, index = worstPlayers[0]
        replacement, budget = replace(player, budget, squad)
        if scraping_level == 0:
            if replacement:
                squad[index] = replacement
                player_points = str(worstData[0])
                match = Matchweek.objects.filter(player=replacement, round=matchcount)
                replacement_points = str(match[0].total_points)
                swap = "{1} for {0}".format(player.name(), replacement.name())
                result_list = "{0}'s points: {2}; {1}'s points: {3}".format(
                    player.name(), replacement.name(), player_points, replacement_points)
            else:
                swap = "None"
                result_list = "{0} was the worst player, but no suitable replacements found.".format(player.name())
        else:
            if replacement:
                squad[index] = replacement
                sentiment_score = worstData[0]
                swap = "{1} for {0}".format(player.name(), replacement.name())
                result_list = r"Tweet: {0}; Sentiment Score: {1:.2f}".format(headlines[index], sentiment_score)
            else:
                swap = "None"
                result_list = "{0} was the worst player, but no suitable replacements found.".format(player.name())

    # return the results
    result_dict['swap'] = swap
    result_dict['details'] = result_list
    result_dict['points'] = points
    result_dict['matchweek'] = matchcount

    return points, squad, budget, result_dict, tweet_url
