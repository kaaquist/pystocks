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
from trigram import Trigram

curr_dir = os.path.dirname(__file__)

class Sentimentanalysis():
	filelabmt = None
	filename = None
	# Word splitter pattern
	pattern_split = None
	afinn = None
	labmtkeywords = None
	engtext = None
	
	
	
	def __init__(self):
		self.pattern_split = re.compile(r"\W+")
		self.filename = os.path.join(curr_dir, 'AFINN/AFINN-111.txt') # This is the newest wordlist.
		"""
		Python supports the creation of anonymous functions (i.e. functions that are not bound to
		a name) at runtime, using a construct called "lambda".
		"""
		self.afinn = dict(map(lambda (w, s): (w, int(s)), [
			ws.strip().split('\t') for ws in open(self.filename) ]))

		self.filelabmt =  os.path.join(curr_dir, 'AFINN/labmt.txt') # This is the newest wordlist.
		self.labmtkeywords = dict(map(lambda(w, s):(w, str(s)), [
			ws.strip().split('\t',1) for ws in open(self.filelabmt)]))
	

	def afinnsentiment(self,text):
		"""
		Returns a float for sentiment strength based on the input text. 
		Positive values are positive valence, negative value are negative valence.
		"""
		
		words = self.pattern_split.split(text.lower())
		sentiments = map(lambda word: self.afinn.get(word, 0), words)
		#check to se if it is not None
		if sentiments:
			# How should you weight the individual word sentiments? 
			# You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
			sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
		else:
			sentiment = 0
		return sentiment
    
    
	def labmtsentiment(self,text):
		"""
		Returns a float for sentiment strength based on the input text.
		Positive values are positive valence, negative value are negative valence. 
		"""
		words = self.pattern_split.split(text.lower())
		sentiments = map(lambda word: self.labmtkeywords.get(word, 0), words)
		#check to se if it is not None
		if sentiments:
			try:
				sumOfSentiments = 0
				valcount = 0
				for tt in sentiments:
					#only uses the first row in labmt
					val = int(str(tt).partition('\t')[0])
					if val != 0:
						sumOfSentiments += val
						valcount += 1
				sentiment = float(sumOfSentiments)/math.sqrt(valcount)
				total = 10222 * valcount
				totalsentiment = float(total)/math.sqrt(valcount)
				sentiment = float(sentiment)/(totalsentiment/100)
			except:
				sentiment  = 0
		else:
			sentiment = 0
		return sentiment
		
	def evaluatetweet(self,tweet):
		"""
		This method takes a tweet and evaluates if it is english or not based on
		n-grams. It returns between 1 for complete similarity, and 0 for utter 
		difference.
		"""
		text = Trigram(tweet)
		if not self.engtext:
			print "Loading"
			self.engtext = Trigram('http://gutenberg.net/dirs/etext05/cfgsh10.txt')
		isitenglish = (text - self.engtext)
		return isitenglish
		

if __name__ == '__main__':
    """ Tests to see that the class actually works as entended. """
    sentimentanalysis = Sentimentanalysis()
    url = "http://ec2-23-22-75-17.compute-1.amazonaws.com:5984/tweets/05fee99baf6ad5869757e6acea000d12"
    response = urllib2.urlopen(url)
    jsonstring = response.read()
    searchresults = json.loads(jsonstring)
    text = searchresults['tweet']
    tweettime = datetime.datetime.fromtimestamp(int(searchresults['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
    print 'tweet:', text
    testt = sentimentanalysis.evaluatetweet(text)
    testt2 = sentimentanalysis.evaluatetweet(text)
    print "---- Test: -----", testt, testt2
    print("%6.2f %s %s" % (sentimentanalysis.afinnsentiment(text), text, tweettime))
    print 'labmt:', sentimentanalysis.labmtsentiment(text)
    
    
       
