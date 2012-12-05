"""
This module creates data structures to be used with the D3 diff graph.
"""

import urllib2
import json
import numpy as np


BASE_URL = 'http://ec2-23-22-75-17.compute-1.amazonaws.com/pystocks/v1/'

def generate_d3(stock_symbol, start=None, end=None):
	"""Generate a JSON structure that makes the data usefull for D3."""
	params = '?'
	if start:
		params += 'start=' + str(start) + '&'
	if end:
		params += 'end=' + str(end) 

	try:
		url = '%squotes/%s%s' % (BASE_URL, stock_symbol, params)
		data = urllib2.urlopen(url).read()
		data = json.loads(data)

		data2 = urllib2.urlopen('%squotes/%s%s' % (BASE_URL, 'MSFT', params)).read()
		data2 = json.loads(data2)
	except:
		# In case we cannot look up data we return None to let caller know
		return None

	# data and data2 must be of equal length. We assume that both data sets end at present day.
	# Therefore we cut of the n first elements of the longest list where n = len_longest - len_shortest.
	diff = abs(len(data) - len(data2))
	if diff:
		if len(data) > len(data2):
			data  = data[diff:]
		elif len(data2) > len(data):
			data2  = data2[diff:]


	values1 = [v[1] for v in data]
	values2 = [v[1] for v in data2];

	quotes, moods = _standardize_data(values1, values2)

	result = []
	i = 0
	for d in data:
		# result.append({'date': ''.join(d[0].split(' ')[0].split('-')), 'quote': d[1], 'mood': data2[i][1]})
		result.append({'date': ''.join(d[0].split(' ')[0].split('-')), 'quote': quotes[i], 'mood': moods[i]})
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
	for i in range(M):
		mean = X[:,i].mean(0) 
		std = X[:,i].std()
		X[:,i] = (X[:,i] - mean)/std

	# Split matrix back into two numpy arrays
	v1 = X[:,0]
	v2 = X[:,1]

	# Return Python lists
	return ([v for v in v1], [v for v in v2])


if __name__ == '__main__':
	print _standardize_data([1,2,3], [100, 220, 300])



