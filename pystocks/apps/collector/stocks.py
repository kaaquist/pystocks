"""
This module fetches closing stock quotes and returns them in a format to be used by the webservice.
"""

import os
tempfile = '/tmp/idk'
os.environ['MPLCONFIGDIR'] = tempfile
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import num2date
from datetime import date, timedelta
import json


def quotes(stock_symbol, start=None, end=None):
	"""Return stock quotes matching the stock symbol between two epoch timestamps."""
	start = start if start else 0
	end = date.fromtimestamp(end) if end else date.today()
	start = date.fromtimestamp(start)
	try:
		quotes = quotes_historical_yahoo(stock_symbol, start, end)
	except:
		# If we cannot find stock symbol return None to let caller know
		return None
	
	dates = [num2date(q[0]) for q in quotes]
	dates = [str(d) for d in dates]
	closing_prices = [q[1] for q in quotes]

	# return {'dates': dates, 'closing_prices': closing_prices}
	return zip(dates, closing_prices)


def _quotes(stock_symbol, start_weeks_delta=4, end_weeks_delta=0, as_json=False, for_d3=False):
	today = date.today()
	start_date = today - timedelta(weeks=start_weeks_delta)
	end_date = today - timedelta(weeks=end_weeks_delta)

	quotes = quotes_historical_yahoo(stock_symbol, start_date, end_date)
	dates = [num2date(q[0]) for q in quotes]
	closing_prices = [q[1] for q in quotes]

	dates = [str(d) for d in dates]
	if for_d3:
		dates = [''.join(d.split(' ')[0].split('-')) for d in dates]
	closing_prices = [float(c) for c in closing_prices]

	result = {'dates': dates, 'closing_prices': closing_prices}

	if as_json:
		return json.dumps(result)
	return result
