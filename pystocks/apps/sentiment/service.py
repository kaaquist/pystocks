"""
This module provides an interface to a webservice that serves sentiment analysis of tweets for companies.
"""

from django.conf import settings
from django.http import HttpResponse
import json
import datetime
from sentiment import Sentimentanalysis


def query_afinn_sentiment_on_company(request, stock_symbol):
	"""
	Return sentiment analysis for a company matching a stock symbol. It is possible to define URL parameters to filter on start
	and end Epoch timestamps. The sentiment is done on a afinn file.
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

	sentimentanalysis = Sentimentanalysis()
	data = tweets.tweets(stock_symbol, start=start, end=end)
	sentafinn={}
	for doc in data:
		#we only want the date to generate a dict with key as date
		tweetdate = datetime.datetime.fromtimestamp(doc['timestamp']).strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]
		tweet = doc['tweet']
		isenglish = sentimentanalysis.evaluatetweet(tweet)
		if isenglish > 0.8:
			sentval = sentimentanalysis.afinnsentiment(tweet)
			if sentafinn.get(tweetdate, 0) == 0:
				sentafinn[tweetdate] = sentval
			else:
				sentafinn[tweetdate] = (sentafinn.get(tweetdate, 0) + sentval)/2
	
	return HttpResponse(json.dumps(sentafinn))
	
def query_labmt_sentiment_on_company(request, stock_symbol):
	"""
	Return sentiment analysis for a company matching a stock symbol. It is possible to define URL parameters to filter on start
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
		return HttpResponse(_error_message('Start and end parameters must be in valid UNIX timestamp format'), status=400, mimetype='application/json')

	sentimentanalysis = Sentimentanalysis()
	data = tweets.tweets(stock_symbol, start=start, end=end)
	sentlabmt={}
	for doc in data:
		#we only want the date to generate a dict with key as date
		tweetdate = datetime.datetime.fromtimestamp(doc['timestamp']).strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]
		tweet = doc['tweet']
		isenglish = sentimentanalysis.evaluatetweet(tweet)
		if isenglish > 0.8:
			sentval = sentimentanalysis.labmtsentiment(tweet)
			if sentafinn.get(tweetdate, 0) == 0:
				sentlabmt[tweetdate] = sentval
			else:
				sentlabmt[tweetdate] = (sentlabmt.get(tweetdate, 0) + sentval)/2
	
	return HttpResponse(json.dumps(sentlabmt))

