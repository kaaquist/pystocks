"""
This module fetches tweets and returns them in a format to be used by the 
webservice.
"""

import json
from django.conf import settings
import pystocks.apps.collector.file_handler as file_handler


def tweets(stock_symbol, start=None, end=None):
    """Return tweets for a stock symbol between two epoch timestamps."""
    company_name = settings.STOCK_SYMBOL_MAPPINGS[stock_symbol]
    try:
        company_file = open(file_handler.filename_for_company(company_name))
    except:
        return {}
    data = json.loads(company_file.read())

    if start or end:
        data = _filter_on_date(data, company_name, start, end)

    return data


def _filter_on_date(data, company_name, start, end):
    """Filter out all tweets whose timestamp is not between start and end."""
    all_tweets = data[company_name]
    filtered_data = []

    for tweet in all_tweets:
        timestamp = tweet['timestamp']

        if start and start > timestamp:
            continue
        if end and end < timestamp:
            continue

        filtered_data.append(tweet)

    return {company_name: filtered_data}


if __name__ == '__main__':
    import os
    import sys
    sys.path.append('/home/django/pystocks/pystocks')
    sys.path.append('/home/django/pystocks')
    os.environ["DJANGO_SETTINGS_MODULE"] = "pystocks.settings"
    print tweets('GOOG')