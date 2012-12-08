"""
This module fetches tweets and returns them in a format to be used by the webservice.
"""

import json
from django.conf import settings
from file_handler import *
import time


def tweets(stock_symbol, start=None, end=None):
	"""Return tweets for a stock symbol between two epoch timestamps."""
	s = time.time()
	# STOCK_SYMBOL_MAPPINGS = { 'GOOG': "Google Inc."}
	company_name = settings.STOCK_SYMBOL_MAPPINGS[stock_symbol]
	# company_name = STOCK_SYMBOL_MAPPINGS[stock_symbol]

	s1 = time.time()
	print s1 - s

	return s1 - s
	f = open(filename_for_company(company_name))
	s2 = time.time()
	print s2 - s1
	data = json.loads(f.read())
	s3 = time.time()
	print s3 - s2

	if start or end:
		data = _filter_on_date(data, company_name, start, end)

	s4 = time.time()
	print s4 - s3

	return data


def _filter_on_date(data, company_name, start, end):
	"""Filter out all tweets whose timestamp is not between start and end."""
	tweets = data[company_name]
	filtered_data = []

	for tweet in tweets:
		timestamp = tweet['timestamp']

		if start and start > timestamp:
			continue
		if end and end < timestamp:
			continue

		filtered_data.append(tweet)

	return {company_name: filtered_data}


if __name__ == '__main__':
	import os
	import sys
	sys.path.append('/home/django/pystocks/pystocks')
	sys.path.append('/home/django/pystocks')
	os.environ["DJANGO_SETTINGS_MODULE"] = "pystocks.settings"
	tweets('GOOG')