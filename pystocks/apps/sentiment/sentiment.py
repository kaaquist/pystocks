#!/usr/bin/python
""" This project file is inspired by the source code from this web site:
http://fnielsen.posterous.com/simplest-sentiment-analysis-in-python-with-af

To get the AFINN word list:
wget http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
unzip imm6010.zip

Since AFINN is a collection of english words we need to make sure that we only look
at the english posts. """

import math
import re
import urllib2
import json
import datetime
import os
import cou
from trigram import Trigram

filename = 'AFINN/AFINN-111.txt' # This is the newest wordlist.
'''
Python supports the creation of anonymous functions (i.e. functions that are not bound to
a name) at runtime, using a construct called "lambda".
'''
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filename) ]))

filelabmt = 'AFINN/labmt.txt' # This is the newest wordlist.

f = open(filelabmt)
labmtkeywords = {}
for line in f.readlines():
    tess = line.split('\t')
    labmtkeywords[tess[0]]= (tess[1],tess[2],tess[3],tess[4],tess[5],tess[6])

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def afinnsentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
        
    else:
        sentiment = 0
    return sentiment
    
    
def labmtsentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: labmtkeywords.get(word, 0), words)
    if sentiments:
        sumOfSentiments = 0
        for tt in sentiments:
            try:
                if tuple(tt) == tt:
                    sumOfSentiments += int(tt[0])
            except TypeError:
                sumOfSentiments += 0
        
        sentiment = float(sumOfSentiments)/math.sqrt(len(sentiments))
        total = 10222 * len(sentiments)
        totalsentiment = float(total)/math.sqrt(len(sentiments))
        sentiment = sentiment/(totalsentiment/100)
    else:
        sentiment = 0
    return sentiment

if __name__ == '__main__':
    url = "http://ec2-23-22-75-17.compute-1.amazonaws.com:5984/tweets/05fee99baf6ad5869757e6acea000d12"
    response = urllib2.urlopen(url)
    jsonstring = response.read()
    searchresults = json.loads(jsonstring)
    text = searchresults['tweet']
    tweettime = datetime.datetime.fromtimestamp(int(searchresults['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
    print 'tweet:', text
    tweet = Trigram(text)
    en = Trigram('http://gutenberg.net/dirs/etext05/cfgsh10.txt')
    isitenglish = (tweet - en)
    print "en - tweet is %s" %(isitenglish)
    print("%6.2f %s %s" % (afinnsentiment(text), text, tweettime))
    print 'labmt:', labmtsentiment(text)
    
    
       
