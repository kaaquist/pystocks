"""
This module saves a dump of the entire database as a 
JSON file structured as a dictionary with companies as keys. 
The file can be used for analysis and visualisation without 
having to query the database.
"""

import json
import io
from django.conf import settings
import urllib2
import urllib
import pystocks.apps.collector.file_handler as file_handler


COMPANY_TO_TWEET_VIEW = 'http://localhost:5984\
/tweets/_design/views/_view/company_to_tweet'


def dump_all_companies():
    """Query all company views and store them as individual JSON files."""
    for company in settings.COMPANIES:
        tweets = _sort_docs(_company_view(company))
        _write_company(company, tweets)


def _write_company(company, tweets):
    """Save a JSON file containing tweets for a company."""
    filename = file_handler.filename_for_company(company)
    print 'Writing to %s' % (filename)
    _write_docs(tweets, filename=filename)


def _company_view(company):
    """Query CouchDB view that returns tweets for a specific company."""
    print 'Querying company: %s' % (company)
    startkey = urllib.urlencode({'startkey': '["' + company + '"]'})
    endkey = urllib.urlencode({'endkey': '["' + company + '",{}]'})
    url = '%s?%s&%s' % (COMPANY_TO_TWEET_VIEW, startkey, endkey)
    data = json.loads(urllib2.urlopen(url).read())
    return [row['value'] for row in data['rows']]


def _write_docs(docs, filename='dummy.json'):
    """Write a list of documents to a file."""
    with io.open(filename, 'wb') as outfile:
        json.dump(docs, outfile)
    print 'Saved file: ' + filename


def _sort_docs(docs):
    """
    Extract the needed information from the full CouchDB 
    documents and return the results as a list.
    """
    result = {}
    for tweet in docs:
        company = tweet['keyword']
        result.setdefault(company, [])
        entry = {'tweet': tweet['tweet'], 'timestamp': tweet['timestamp']}
        result[company].append(entry)
    return result


if __name__ == '__main__':
    dump_all_companies()





