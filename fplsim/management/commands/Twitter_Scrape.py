from django.core.management.base import BaseCommand, CommandError
from fplsim.models import Player, Tweet
import fplsim.tweet_scraper as twitter
import fplsim.sentiment_analysis as sentiment
import os, csv, re
import personal_website.settings as settings


class Command(BaseCommand):
    help = 'Scrapes twitter data to acquire tweets with negative sentiment'

    def add_arguments(self, parser):
        parser.add_argument('player_id', nargs=1, type=int)
        parser.add_argument('--load', action='store_true')

    def handle(self, *args, **options):
        load = options['load']
        if load:
            self.loadData()
            self.stdout.write(self.style.SUCCESS(
                'Load Successful'))
        else:
            id = options['player_id'][0]
            for player in Player.objects.filter(id__gt=id):
                try:
                    self.getTweets(player)
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully acquired tweets for player %s' % player.name()))
                except Exception as inst:
                    raise CommandError('Error occurred. %s' % inst)

    def getTweets(self, player):
        dates = ['2017-08-13', '2017-08-19', '2017-08-26', '2017-09-11', '2017-09-16',
                 '2017-09-23', '2017-09-30', '2017-10-14', '2017-10-20', '2017-10-28',
                 '2017-11-04', '2017-11-19', '2017-11-24', '2017-11-29', '2017-12-03',
                 '2017-12-09', '2017-12-13', '2017-12-16', '2017-12-23', '2017-12-31']
        searcher = twitter.Searcher()
        worst_tweets = []
        module_dir = settings.STATICFILES_DIRS
        fname = str(player.id) + '.csv'
        file_path = os.path.join(module_dir[0], fname)

        with open(file_path, 'w+', newline='') as f:
            writer = csv.writer(f)
            for matchcount in range(5):
                tweets, urls = searcher.search(player, 5, dates[matchcount], dates[matchcount + 1])
                sentimentList = []
                if tweets:
                    for tweet in tweets:
                        sentimentList.append(sentiment.sentiment(tweet))
                    worst = min(sentimentList)
                    worstIndex = sentimentList.index(worst)
                    tweet = tweets[worstIndex]
                    data = [tweet,
                            sentimentList[worstIndex],
                            urls[worstIndex]]
                    writer.writerow(data)
                else:
                    data = ['', 2]
                    writer.writerow(data)
        f.close()

    def loadData(self):
        module_dir = settings.STATICFILES_DIRS
        players = Player.objects.all()
        for player in players:
            fname = str(player.id) + '.csv'
            file_path = os.path.join(module_dir[0], fname)
            if os.path.exists(file_path):
                with open(file_path, newline='') as f:
                    data = csv.reader(f, delimiter =',')
                    for matchweek, row in enumerate(data):
                        if len(row[0]) > 0:
                            text = row[0]
                            tweet = Tweet.objects.filter(player=player,text=text,sentiment=float(row[1]),
                                                         round=matchweek+1,url=row[2])
                            if tweet:
                                try:
                                    Tweet(player=player,text=text,sentiment=float(row[1]),round=matchweek+1,url=row[2]).save()
                                except:
                                    self.stdout.write(self.style.SUCCESS(
                                        'Could not create {0}'.format(text)))
                            self.stdout.write(self.style.SUCCESS(
                                'Successfully created tweet {0}'.format(text)))