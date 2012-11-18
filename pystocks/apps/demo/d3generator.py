"""
This module creates data structures to be used with the D3 diff graph.
"""

import urllib2
import json


BASE_URL = 'http://ec2-23-22-75-17.compute-1.amazonaws.com/v1/'

def generate_d3(stock_symbol, start=None, end=None):
	params = '?'
	if start:
		params += 'start=' + str(start) + '&'
	if end:
		params += 'end=' + str(end) 

	# url = '%squotes/%s?start=%s' % (BASE_URL, stock_symbol, START_DATE)
	url = '%squotes/%s%s' % (BASE_URL, stock_symbol, params)
	data = urllib2.urlopen(url).read()
	data = json.loads(data)

	data2 = urllib2.urlopen('%squotes/%s%s' % (BASE_URL, 'IBM', params)).read()
	data2 = json.loads(data2)

	result = []
	i = 0
	for d in data:
		result.append({'date': ''.join(d[0].split(' ')[0].split('-')), 'quote': d[1], 'mood': data2[i][1]})
		i += 1

	return json.dumps(result)
