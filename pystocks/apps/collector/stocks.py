"""
This module fetches closing stock quotes and returns 
them in a format to be used by the webservice.
"""

import os
os.environ['MPLCONFIGDIR'] = '/tmp/idk'
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import num2date
from datetime import date


def quotes(stock_symbol, start=None, end=None):
    """
    Return stock quotes matching the stock 
    symbol between two epoch timestamps.
    """
    start = start if start else 0
    end = date.fromtimestamp(end) if end else date.today()
    start = date.fromtimestamp(start)
    try:
        stocks = quotes_historical_yahoo(stock_symbol, start, end)
    except:
        # If we cannot find stock symbol return None to let caller know
        return None
    
    dates = [num2date(q[0]) for q in stocks]
    dates = [str(d) for d in dates]
    closing_prices = [q[1] for q in stocks]

    ret = {}
    for pair in zip(dates, closing_prices):
        ret[pair[0].split(' ')[0]] = pair[1]
    return ret


if __name__ == '__main__':
    print quotes('GOOG')