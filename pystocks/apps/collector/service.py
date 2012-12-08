"""
This module provides the interface to the webservice that serves the tweets and quotes for companies.
"""

from django.conf import settings
from django.http import HttpResponse
import json
import stocks
import tweets


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
	except:
		return HttpResponse(_error_message('Start and end parameters must be in valid UNIX timestamp format'), status=400, mimetype='application/json')

	# return HttpResponse('hell')
	data = tweets.tweets(stock_symbol, start=start, end=end)

	return HttpResponse(json.dumps(data))


def company_list(request):
	"""Return a list of companies and their stock symbols."""
	companies = [{'name': v, 'symbol': k} for k,v in settings.STOCK_SYMBOL_MAPPINGS.items()]
	return HttpResponse(json.dumps(companies))


def quotes(request, stock_symbol):
	"""Return stock quotes between two epoch timestamps. If no timestamps are given, distant past and today will be used."""
	start = request.GET.get('start')
	try:
		if start:
			start = int(start)
		end = request.GET.get('end')
		if end:
			end = int(end)
	except:
		return HttpResponse(_error_message('Start and end parameters must be in valid UNIX timestamp format'), status=400, mimetype='application/json')

	data = stocks.quotes(stock_symbol, start=start, end=end)
	if data == None:
		return HttpResponse(_error_message('Could not find stocksymbol %s' % (stock_symbol)), status=404, mimetype='application/json')

	return HttpResponse(json.dumps(data))


def _error_message(error):
	return json.dumps({'error': error})


