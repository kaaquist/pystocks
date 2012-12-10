"""
This module provides an interface to a webservice that serves 
sentiment analysis of tweets for companies.
"""

from django.http import HttpResponse
import json
from pystocks.apps.sentiment.tweet_sentiment import sentiments


def afinn_sentiment_on_company(request, stock_symbol):
    """
    Return sentiment analysis for a company matching a stock symbol. It is 
    possible to define URL parameters to filter on start and end Epoch timestamps.
    The sentiment is done on a afinn file.
    """
    try:
        start = request.GET.get('start')
        if start:
            start = int(start)
        end = request.GET.get('end')
        if end:
            end = int(end)
    except:
        error = _error_message('Start and end parameters must \
            be in valid UNIX timestamp format')
        return HttpResponse(error, status=400, mimetype='application/json')

    sentiment_data = sentiments(stock_symbol, start=start, end=end)
    return HttpResponse(json.dumps(sentiment_data), mimetype='application/json')
    
def labmt_sentiment_on_company(request, stock_symbol):
    """
    Return sentiment analysis for a company matching a stock symbol. 
    It is possible to define URL parameters to filter on start
    and end Epoch timestamps. The sentiment is done on a labmt file.
    """
    try:
        start = request.GET.get('start')
        if start:
            start = int(start)
        end = request.GET.get('end')
        if end:
            end = int(end)
    except:
        error = _error_message('Start and end parameters must\
         be in valid UNIX timestamp format')
        return HttpResponse(error, status=400, mimetype='application/json')

    s_data = sentiments(stock_symbol, method='labmt', start=start, end=end)
    return HttpResponse(json.dumps(s_data), mimetype='application/json')


def _error_message(error):
    """Creates a standard JSON error message."""
    return json.dumps({'error': error})
