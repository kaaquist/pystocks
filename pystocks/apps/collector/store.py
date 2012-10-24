"""
Database module for connecting to and storing documents in the CouchDB database.
"""

import couchdb
import time

_server = couchdb.Server()
cloudant = _server['tweets']

_docs_to_store = []

UPDATE_CHUNK = 1000

def store_tweet(tweet, keyword):
	"""Store a tweet in the database with a keyword identifying the company the tweet mentions."""
	global _docs_to_store
	doc = {'tweet': tweet, 'keyword': keyword, 'timestamp': int(time.time())}
	_docs_to_store.append(doc)
	if len(_docs_to_store) == UPDATE_CHUNK:
		cloudant.update(_docs_to_store)
		_docs_to_store = []