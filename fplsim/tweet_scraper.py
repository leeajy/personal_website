from tweepy import OAuthHandler
from tweepy import API
from tweepy import TweepError
import os, re
import subprocess
import personal_website.settings as settings



class Authenticator:

    def authenticate(self):
        TWITTER_API_KEY = settings.TWITTER_API_KEY
        TWITTER_API_SECRET_KEY = settings.TWITTER_API_SECRET_KEY
        TWITTER_ACCESS_TOKEN = settings.TWITTER_ACCESS_TOKEN
        TWITTER_ACCESS_TOKEN_SECRET = settings.TWITTER_ACCESS_TOKEN_SECRET
        TWITTER_BEARER_TOKEN = settings.TWITTER_BEARER_TOKEN
        auth = OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return auth


class Searcher:
    """
        Class to search for tweets. Initializes with authentication and outputs tweets
        The player_list input will take in a str of players. (Call the function after
        acquiring strings from Players model:
        (ex. testPlayers = list(map(str, Player.objects.filter(position=4)[0:3]))
    """

    def __init__(self):
        self.authenticator = Authenticator()
        self.auth = self.authenticator.authenticate()

    # original method, this does not work for tweets going back before a week from today
    def search_7day(self, player, max_count, matchdate):
        api = API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        tweets = []
        filters = ' filter:safe'
        filter_query = player.name() + filters
        try:
            new_tweets = api.search(q=filter_query, lang="en", count=max_count,
                                    until=matchdate, result_type='popular')
            for result in new_tweets:
                tweet = self.cleaner(tweet.text)
                tweets.append(tweet)
        except TweepError as e:
            # Just exit if any error
            print(str(e))
            return ''
        finally:
            return tweets

    def search(self, player, max_count, since_date, until_date):
        filters = ' filter:safe since:{0} until:{1}'.format(since_date, until_date)
        filter_query = player.name() + filters + ' list:LeeAntonio55/PremierLeagueNews'

        p = subprocess.Popen('snscrape twitter-search "{0}"'.format(filter_query), stdout=subprocess.PIPE, shell=True)
        output =[]
        urls = []
        for i in range(max_count):
            out = p.stdout.readline()
            out = out.decode('utf-8')
            out = out.strip('\r\n')
            urls.append(out)
            out = out.split(sep='/')[-1]
            output.append(out)
        p.kill()


        api = API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        tweets = []
        try:
            new_tweets = api.statuses_lookup(output,False)
            for tweet in new_tweets:
                tweet = self.cleaner(tweet.text)
                whitelist = set("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.,;:'")
                tweet = ''.join(filter(whitelist.__contains__, tweet))
                tweets.append(tweet)
        except TweepError as e:
            # Just exit if any errors
            print(str(e))
            tweet.append('')
        finally:
            return tweets, urls

    def cleaner(self, tweet):
        tweet = re.sub(r'^RT[\s]+', '', tweet)
        tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
        tweet = re.sub(r'#', '', tweet)
        tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet)
        return tweet
