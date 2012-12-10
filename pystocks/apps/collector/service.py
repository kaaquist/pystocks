"""
This module provides the interface to the webservice that serves the 
tweets and quotes for companies.
"""

from django.conf import settings
from django.http import HttpResponse
import json
import pystocks.apps.collector.stocks as stocks
import pystocks.apps.collector.tweets as tweets


def query_company(request, stock_symbol):
    """
    Return tweets for company matching a stock symbol. It is possible to define URL parameters to filter on start
    and end Epoch timestamps.
    """
    try:
        start = request.GET.get('start')
        if start:
            start = int(start)
        end = request.GET.get('end')
        if end:
            end = int(end)
    except Exception:
        error = _error_message('Start and end parameters must be \
         in valid UNIX timestamp format')
        return HttpResponse(error, status=400, mimetype='application/json')

    # return HttpResponse('hell')
    data = tweets.tweets(stock_symbol, start=start, end=end)

    return HttpResponse(json.dumps(data))


def company_list(request):
    """Return a list of companies and their stock symbols."""
    items = settings.STOCK_SYMBOL_MAPPINGS.items()
    companies = [{'name': v, 'symbol': k} for k, v in items]
    return HttpResponse(json.dumps(companies), mimetype='application/json')


def quotes(request, stock_symbol):
    """
    Return stock quotes between two epoch timestamps.
    If no timestamps are given, distant past and today will be used.
    """
    start = request.GET.get('start')
    try:
        if start:
            start = int(start)
        end = request.GET.get('end')
        if end:
            end = int(end)
    except Exception:
        error = _error_message('Start and end parameters must be \
            in valid UNIX timestamp format')
        return HttpResponse(error, status=400, mimetype='application/json')

    data = stocks.quotes(stock_symbol, start=start, end=end)
    if data == None:
        error = _error_message('Could not find stocksymbol %s' % (stock_symbol))
        return HttpResponse(error, status=404, mimetype='application/json')

    return HttpResponse(json.dumps(data))


def _error_message(error):
    """Creates a standard JSON error message."""
    return json.dumps({'error': error})


