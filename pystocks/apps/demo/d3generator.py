import urllib2
import json

START_DATE = ''
BASE_URL = 'http://ec2-23-22-75-17.compute-1.amazonaws.com/v1/'

def generate_d3(stock_symbol):
	url = '%squotes/%s?start=%s' % (BASE_URL, stock_symbol, START_DATE)
	data = urllib2.urlopen(url).read()
	data = json.loads(data)

	data2 = urllib2.urlopen('%squotes/%s?start=%s' % (BASE_URL, 'IBM', START_DATE)).read()
	data2 = json.loads(data2)

	result = []
	i = 0
	for d in data:
		# result.append({'date': str(d[0]), 'quote': d[1], 'mood': d[1]})
		# result.append({'date': ''.join('2012-10-22 00:00:00+00:00'.split(' ')[0].split('-')), 'quote': d[1], 'mood': d[1]})
		result.append({'date': ''.join(d[0].split(' ')[0].split('-')), 'quote': d[1], 'mood': data2[i][1]})
		i += 1

	# dates = [d[1] for d in data]
	# quotes = [d[0] for d in data]

	return json.dumps(result)


# def _quotes(stock_symbol, start_weeks_delta=4, end_weeks_delta=0, as_json=False, for_d3=False):
# 	today = date.today()
# 	start_date = today - timedelta(weeks=start_weeks_delta)
# 	end_date = today - timedelta(weeks=end_weeks_delta)

# 	quotes = quotes_historical_yahoo(stock_symbol, start_date, end_date)
# 	dates = [num2date(q[0]) for q in quotes]
# 	closing_prices = [q[1] for q in quotes]

# 	dates = [str(d) for d in dates]
# 	if for_d3:
# 		dates = [''.join(d.split(' ')[0].split('-')) for d in dates]
# 	closing_prices = [float(c) for c in closing_prices]

# 	result = {'dates': dates, 'closing_prices': closing_prices}

# 	if as_json:
# 		return json.dumps(result)
# 	return result