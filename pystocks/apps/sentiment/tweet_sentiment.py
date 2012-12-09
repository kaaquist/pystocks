import json
from file_handler import *
from django.conf import settings
from datetime import date


def sentiments(stock_symbol, method='afinn', start=None, end=None):
	"""Return tweet sentiments for a stock symbol between two epoch timestamps."""
	company_name = settings.STOCK_SYMBOL_MAPPINGS[stock_symbol]
	try:
		f = open(filename_for_company(method, company_name))
	except:
		return {}
	data = json.loads(f.read())

	if start or end:
		data = _filter_on_date(data, company_name, start, end)

	return data


def _filter_on_date(data, company_name, start, end):
	"""Filter out all sentiments whose timestamp is not between start and end."""
	filtered_data = {}

	start_date = date.fromtimestamp(1)
	try:
		start_date = date.fromtimestamp(start)
	except:
		pass
	
	end_date = date.fromtimestamp(10e10)
	try:
		end_date = date.fromtimestamp(end)
	except:
		pass

	for s_date, sentiment in data.items():
		splits = s_date.split('-')
		year = int(splits[0])
		month = int(splits[1])
		day = int(splits[2])

		d = date(year, month, day)

		if d > end_date:
			continue
		if d < start_date:
			continue

		filtered_data[s_date] = sentiment

	return {company_name: filtered_data}

if __name__ == '__main__':
	import os
	import sys
	sys.path.append('/home/django/pystocks/pystocks')
	sys.path.append('/home/django/pystocks')
	os.environ["DJANGO_SETTINGS_MODULE"] = "pystocks.settings"
	print sentiments('AMGN', start=1354296768, end=1354555968)



