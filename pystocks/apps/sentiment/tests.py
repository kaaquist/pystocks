# -*- coding: utf-8 -*-
"""
Test the sentiment API and the sentiment calculations.
"""
from django.test import TestCase
import pystocks.apps.sentiment.tweet_sentiment as tweet_sentiment
from pystocks.apps.sentiment.sentiment import Sentimentanalysis
import time

class SentimentAPITestCase(TestCase):
    def test_content(self):
        """Test that the sentiment API returns something"""
        data = tweet_sentiment.sentiments('GOOG', start=time.time()-864000, end=time.time())
        self.assertTrue(len(data) > 0)

    def test_content_no_params(self):
        """
        Test that the sentiment API returns something 
        when start and end are not specified
        """
        data = tweet_sentiment.sentiments('GOOG')
        self.assertTrue(len(data) > 0)

    def test_non_content(self):
        """Test that the sentiment API returns nothing when the time range is wrong"""
        data = tweet_sentiment.sentiments('GOOG', start=time.time(), end=time.time()-864000)
        self.assertEqual(len(data), 0)



class SentimentTestCase(TestCase):
    def test_is_english(self):
        """
        Test that the sentiment class can classify text as english.
        """
        sentimentanalysis = Sentimentanalysis()
        tweet = 'This is a dumb tweet'
        score = sentimentanalysis.evaluatetweet(tweet)
        self.assertTrue(score > 0.9)

    def test_special_characters(self):
        """
        Test that sentiment class will not break on special characters.
        """
        sentimentanalysis = Sentimentanalysis()
        strange_tweet = 'ÅÚÍÎÏ””ŒER""øøø…weqrwqerqw wwcrqwe lchrjqekwchr http://asf.adfasdfæ…øåœœåÅ'
        sentimentanalysis.afinnsentiment(strange_tweet)
        sentimentanalysis.labmtsentiment(strange_tweet)
        # If we made it this far we passed the test
        self.assertTrue(True)





