"""
This module creates data structures to be used with the D3 diff graph.
"""

import urllib2
import json
import numpy as np


BASE_URL = 'http://ec2-23-22-75-17.compute-1.amazonaws.com/pystocks/v1/'

def generate_d3(stock_symbol, method='afinn', start=None, end=None):
	"""
	Generate a JSON structure that makes the data usefull for D3.

	Possible methods:
	afinn
	labmt

	"""
	params = '?'
	if start:
		params += 'start=' + str(start) + '&'
	if end:
		params += 'end=' + str(end) 

	# try:
	url = '%squotes/%s%s' % (BASE_URL, stock_symbol, params)
	data = urllib2.urlopen(url).read()
	data = json.loads(data)

	url2 = '%ssentiment/%s/%s%s' % (BASE_URL, method, stock_symbol, params)
	data2 = urllib2.urlopen(url2).read()
	data2 = json.loads(data2)

	print data2.keys()
	new_data = {}
	new_data2 = {}
	for key in data.keys():
		if data2.get(key):
			new_data[key] = data[key]
			new_data2[key] = data2[key]

	data = new_data
	data2 = new_data2

	values1 = [data[key] for key in sorted(data)]
	values2 = [data2[key] for key in sorted(data2)]

	quotes, moods = _standardize_data(values1, values2)

	result = []
	i = 0
	for d in sorted(data):
		result.append({'date': ''.join(d.split('-')), 'quote': quotes[i], 'mood': moods[i]})
		i += 1
	return json.dumps(result)


def _standardize_data(data1, data2):
	"""Standardize two python lists."""

	# Convert lists to numpy arrays
	a = np.array(data1)
	b = np.array(data2)

	# Get number of entries in lists
	nof_entries = (len(a))

	# Initialize empty matrix
	X = np.empty((nof_entries, 2))

	# Populate matrix with list data
	for i in range(nof_entries):
		X[i,0] = a[i]
		X[i,1] = b[i]

	# Standardize data
	N, M = np.shape(X)
	print X
	for i in range(M):
		mean = X[:,i].mean(0) 
		std = X[:,i].std()
		val = 0.5
		if std:
			val = (X[:,i] - mean)/std
		X[:,i] = val

	# Split matrix back into two numpy arrays
	v1 = X[:,0]
	v2 = X[:,1]

	# Return Python lists
	return ([v for v in v1], [v for v in v2])


if __name__ == '__main__':
	# print _standardize_data([1,2,3], [100, 220, 300])
	generate_d3('NFLX')#, start='1354715385')



