"""
This module performs sentiment analysis on all 
companies for the past three days and stores it in a JSON file.
"""

import json
import io
import datetime
from django.conf import settings
import pystocks.apps.collector.tweets as tweets
from pystocks.apps.sentiment.file_handler import filename_for_company
from pystocks.apps.sentiment.sentiment import Sentimentanalysis


def dump_all():
    """
    Dump all sentiment scores for both labmt and afinn.
    """
    dump()
    dump(method='labmt')

def dump(method='afinn'):
    """
    Do sentiment analysis on all tweets for all companies and 
    write the results to a file.
    """
    sentimentanalysis = Sentimentanalysis()
    
    sent_method = None
    if method == 'afinn':
        sent_method = sentimentanalysis.afinnsentiment
    elif method == 'labmt':
        sent_method = sentimentanalysis.labmtsentiment      

    for stock_symbol, company in settings.STOCK_SYMBOL_MAPPINGS.items():
        print 'Company: ' + str(company)
        data = tweets.tweets(stock_symbol)
        sentiment = {}
        filename = filename_for_company(method, company)
        print 'Filename: ' + str(filename)
        try:
            sentiment = json.loads(open(filename).read())
        except:
            print 'No file data'

        for key in data:
            docs = data[key]
            first = True
            count = 0
            for doc in docs:
                count += 1
                print 'Iterating %d of %d' % (count, len(docs))
                tweetdate = datetime.datetime.fromtimestamp(doc['timestamp']).strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]
                if first:
                    sentiment[tweetdate] = 0
                    first = False
                tweet = doc['tweet']
                isenglish = sentimentanalysis.evaluatetweet(tweet)
                if isenglish > 0.8:
                    sentval = sent_method(tweet)
                    if sentiment.get(tweetdate, 0) == 0:
                        sentiment[tweetdate] = sentval
                    else:
                        sentiment[tweetdate] = (sentiment.get(tweetdate, 0) + sentval)/2

        with io.open(filename, 'wb') as outfile:
            json.dump(sentiment, outfile)
        print 'Saved file: ' + filename

