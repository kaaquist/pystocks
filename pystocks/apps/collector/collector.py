"""
This module implements a custom Twitter stream listener which 
filters on a number of companies and their corresponding keywords.
The module will ignore stream errors and keep it self alive at all 
costs. Only successfull responses are handled.

Based on article by Peter Hoffmann: 
http://peter-hoffmann.com/2012/simple-twitter-streaming-api-access-with-python-and-oauth.html
"""

import tweepy
import pystocks.apps.collector.store as store
from django.conf import settings


class CustomStreamListener(tweepy.StreamListener):
    """
    Extend tweepy.StreamListener. Ignore everything but successfull responses.
    Store successfull responses in CouchDB.
    """

    def handle_tweet(self, tweet):
        """
        Iterate companies and store the tweet 
        for each company mentioned in the tweet.
        """
        for company in settings.COMPANIES:
            for keyword in settings.COMPANIES[company]:
                if keyword in tweet:
                    store.store_tweet(tweet, company)
                    break # go to next company

    def on_status(self, status):
        """Called upon successfull retrieval of tweet."""
        self.handle_tweet(status.text)
    
    def on_error(self, status_code):
        """
        Called upon failed request. 
        This will be ignored to keep the stream alive.
        """
        return True # Don't kill the stream

    def on_timeout(self):
        """
        Called upon timed out request. 
        This will be ignored to keep the stream alive.
        """
        return True # Don't kill the stream

def collect(keywords=settings.COMPANIES):
    """
    Start the stream collection.

    Keyword arguments:
    keywords -- the list of words to use in the stream filtering (default settings.COMPANIES)

    """
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    # api = tweepy.API(auth)
    tweepy.API(auth)
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(track=keywords)

def get_companies_and_stock_symbols():
    """Make a list of tuples containing company names and stock symbols."""
    return [(c, settings.COMPANIES[c][0]) for c in settings.COMPANIES]





