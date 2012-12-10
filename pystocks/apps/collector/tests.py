"""
Test of the Core APIs. I.e. Stock quote API and Tweet API.
"""
from django.test import TestCase
import pystocks.apps.collector.stocks as stocks
import pystocks.apps.collector.tweets as tweets
import time

class StocksTestCase(TestCase):
    def test_content(self):
        """Test that the stock API returns something"""
        data = stocks.quotes('GOOG', start=time.time()-864000, end=time.time())
        self.assertTrue(len(data) > 0)

    def test_content_no_params(self):
        """
        Test that the stock API returns something 
        when start and end are not specified
        """
        data = stocks.quotes('GOOG')
        self.assertTrue(len(data) > 0)

    def test_non_content(self):
        """Test that the stock API returns nothing when the time range is wrong"""
        data = stocks.quotes('GOOG', start=time.time(), end=time.time()-864000)
        self.assertTrue(data is None)


class TweetsTestCase(TestCase):
    def test_content(self):
        """Test that the tweet API returns something"""
        data = tweets.tweets('GOOG', start=time.time()-864000, end=time.time())
        self.assertTrue(len(data['Google Inc.']) > 0)

    def test_content_no_params(self):
        """
        Test that the tweets API returns something 
        when start and end are not specified
        """
        data = tweets.tweets('GOOG')
        self.assertTrue(len(data['Google Inc.']) > 0)

    def test_non_content(self):
        """Test that the tweet API returns an empty array when the time range is wrong"""
        data = tweets.tweets('GOOG', start=time.time(), end=time.time()-864000)
        self.assertEqual(len(data['Google Inc.']), 0)


        