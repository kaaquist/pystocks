"""
This module fetches tweets and returns them in a format to be used by the webservice.
"""

import json
from django.conf import settings
from file_handler import *


def tweets(stock_symbol, start=None, end=None):
	"""Return tweets for a stock symbol between two epoch timestamps."""
	company_name = settings.STOCK_SYMBOL_MAPPINGS[stock_symbol]
	f = open(filename_for_company(company_name))
	data = json.loads(f.read())

	if start or end:
		data = _filter_on_date(data, company_name, start, end)

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