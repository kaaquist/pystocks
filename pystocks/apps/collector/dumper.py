"""
This module saves a dump of the entire database as a JSON file structured as a dictionary with companies as keys. 
The file can be used for analysis and visualisation without having to query the database.
"""

import couchdb
import json
import io
import store
import urllib2
import time

FILENAME = 'tweets.json'
"""Filename to write dump to."""

http_times = []
def http():
	"""Query the database using pure HTTP."""
	global http_times
	print 'Getting headers'
	start = time.time()
	headers = json.loads(urllib2.urlopen('http://localhost:5984/tweets/_all_docs').read())['rows']
	print 'Got headers'
	docs = []
	c = 0
	for header in headers:
		doc = json.loads(urllib2.urlopen('http://localhost:5984/tweets/' + header['key']).read())
		docs.append(doc)
		c += 1
		if c % 100 == 0:
			print '%d of %d' % (c, len(headers))
		# if c == 10: break
	end = time.time()
	t = end - start
	http_times.append(t)
	print 'Done'
	print 'Time: ' + str(t)

	return docs

couch_times = []
def couch():
	"""Query the database using the Python CouchDB module."""
	global couch_times
	print 'Starting CouchDB'
	c = 0
	docs = []
	start = time.time()
	for doc_key in store.cloudant:
		doc = store.cloudant[doc_key]
		docs.append(doc)
		c += 1
		if c % 100 == 0:
			print '%d of %d' % (c, len(store.cloudant))
		# if c == 1000: break
	end = time.time()
	t = end - start
	couch_times.append(t)
	print 'Done'
	print 'Time: ' + str(t)

	return docs


def write_docs(docs, filename=FILENAME):
	"""Write a list of documents to a file."""
	print 'Writing file'
	with io.open(FILENAME, 'wb') as outfile:
		# outfile.write(json.dumps(docs))
		# docs = sort_docs(docs)
		json.dump(docs, outfile)
	print 'Saved file: ' + filename


def sort_docs(docs):
	result = {}
	for tweet in docs:
		# tweet = json.loads(tweet)
		company = tweet['keyword']
		result.setdefault(company, [])
		entry = {'tweet': tweet['tweet'], 'timestamp': tweet['timestamp']}
		result[company].append(entry)
	return result

def read_dump():
	with io.open(FILENAME, 'rb') as json_file:
		return json.loads(json_file.read())

if __name__ == '__main__':

	write_docs(sort_docs(http()))

	# docs = read_dump()
	# print sort_docs(docs)['Green Mountain Coffee Roasters, Inc.']

	# for i in range(10):
	# 	couch()
	# 	# http()
	# print 'HTTP times:'
	# print http_times
	# print
	# print 'CouchDB time:'
	# print couch_times

	# dif = http_times - couch_times
	# print
	# print 'Diff: ' + str(dif)





