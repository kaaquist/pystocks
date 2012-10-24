"""
This module implements a custom Twitter stream listener which filters on a number of companies and their corresponding keywords.
The module will ignore stream errors and keep it self alive at all costs. Only successfull responses are handled.
"""

import sys
import tweepy
import store


CONSUMER_KEY = 'hLnoFmPOO3RJK7UEsjNg'
CONSUMER_SECRET = 'A9CaQhzNStdm0e6Lwe6CrRg6lo4e3HtSl1TNnh6Z66w'
ACCESS_TOKEN = '45764918-r1TnkRYeFMkrZbixWtekKTNguBzpgBMhzFQSynOIw'
ACCESS_TOKEN_SECRET = 'xGuINQVRkqsK31zUdxDoH6oylD2PREnaJ9eXgyA'

# Nasdaq-100
COMPANIES = {
"Activision Blizzard, Inc": ["#ATVI", "Activision", "Blizzard"],
"Adobe Systems Incorporated": ["#ADBE", "Adobe"],
"Akamai Technologies, Inc.": ["#AKAM", "Akami"],
"Alexion Pharmaceuticals, Inc.": ["#ALXN", "Alexion"],
"Altera Corporation": ["#ALTR", "Altera"],
"Amazon.com, Inc.": ["#AMZN", "Amazon", "Amazon.com"],
"Amgen Inc.": ["#AMGN", "Amgen"],
"Apollo Group, Inc.": ["#APOL"],
"Apple Inc.": ["#AAPL", "Apple"],
"Applied Materials, Inc.": ["#AMAT"],
"Autodesk, Inc.": ["#ADSK", "Autodesk"],
"Automatic Data Processing, Inc.": ["#ADP"],
"Avago Technologies Limited": ["#AVGO"],
"Baidu, Inc.": ["#BIDU", "Baidu"],
"Bed Bath & Beyond Inc.": ["#BBBY", "Bed Bath & Beyond"],
"Biogen Idec Inc": ["#BIIB", "Biogen"],
"BMC Software, Inc.": ["#BMC", "BMC Software"],
"Broadcom Corporation": ["#BRCM", "Broadcom"],
"C.H. Robinson Worldwide, Inc.": ["#CHRW", "C.H. Robinson", "CH Robinson"],
# "CA Inc.": ["#CA"],
"Celgene Corporation": ["#CELG", "Celgene"],
"Cerner Corporation": ["#CERN", "Cerner"],
"Check Point Software Technologies Ltd.": ["#CHKP", "Check Point Software"],
"Cisco Systems, Inc.": ["#CSCO", "Cisco"],
"Citrix Systems, Inc.": ["#CTXS", "Citrix"],
"Cognizant Technology Solutions Corporation": ["#CTSH", "Cognizant"],
"Comcast Corporation": ["#CMCSA", "Comcast"],
"Costco Wholesale Corporation": ["#COST", "Costco"],
"Dell Inc.": ["#DELL", "Dell"],
"DENTSPLY International Inc.": ["#XRAY", "DENTSPLY"],
"DIRECTV": ["#DTV", "DIRECTV"],
"Dollar Tree, Inc.": ["#DLTR", "Dollar Tree"],
"eBay Inc.": ["#EBAY", "eBay"],
"Electronic Arts Inc.": ["#ERTS", "Electronic Arts", "EA", "E.A."],
"Expedia, Inc.": ["#EXPE", "Expedia"],
"Expeditors International of Washington, Inc.": ["#EXPD", "Expeditors International of Washington"],
"Express Scripts, Inc.": ["#ESRX", "Express Scripts"],
"F5 Networks, Inc.": ["#FFIV", "F5 Networks"],
"Fastenal Company": ["#FAST", "Fastenal"],
"Fiserv, Inc.": ["#FISV", "Fiserv"],
"Flextronics International Ltd.": ["#FLEX", "Flextronics"],
"Fossil, Inc.": ["#FOSL"],
"Garmin Ltd.": ["#GRMN", "Garmin"],
"Gilead Sciences, Inc.": ["#GILD", "Gilead"],
"Google Inc.": ["#GOOG", "Google"],
"Green Mountain Coffee Roasters, Inc.": ["#GMCR", "Green Mountain Coffee"],
"Henry Schein, Inc.": ["#HSIC", "Henry Schein"],
"Infosys Limited": ["#INFY", "Infosys"],
"Intel Corporation": ["#INTC", "Intel"],
"Intuit Inc.": ["#INTU", "Intuit"],
"Intuitive Surgical, Inc.": ["#ISRG", "Intuitive Surgical"],
"KLA-Tencor Corporation": ["#KLAC", "KLA-Tencor"],
"Kraft Foods Inc.": ["#KFT", "Kraft Foods"],
"Lam Research Corporation": ["#LRCX", "Lam Research"],
"Liberty Media Corporation": ["#LINTA", "Liberty Media"],
"Life Technologies Corporation": ["#LIFE", "Life Technologies"],
"Linear Technology Corporation": ["#LLTC", "Linear Technology"],
"Marvell Technology Group Ltd.": ["#MRVL", "Marvell"],
"Mattel, Inc.": ["#MAT", "Mattel"],
"Maxim Integrated Products, Inc.": ["#MXIM", "Maxim"],
"Microchip Technology Incorporated": ["#MCHP", "Microchip Technology Incorporated"],
"Micron Technology, Inc.": ["#MU", "Micron"],
"Microsoft Corporation": ["#MSFT", "Microsoft"],
"Monster Beverage Corporation": ["#MNST", "Monster Beverage"],
"Mylan Inc.": ["#MYL", "Mylan"],
"NetApp, Inc.": ["#NTAP", "NetApp"],
"Netflix, Inc.": ["#NFLX", "Netflix"],
"Nuance Communications, Inc.": ["#NUAN", "Nuance"],
"NVIDIA Corporation": ["#NVDA", "NVIDIA"],
"News Corporation": ["#NWSA", "News Corporation"],
"O'Reilly Automotive, Inc.": ["#ORLY", "O'Reilly"],
"Oracle Corporation": ["#ORCL", "Oracle"],
"PACCAR Inc.": ["#PCAR", "PACCAR"],
"Paychex, Inc.": ["#PAYX", "Paychex"],
"priceline.com Incorporated": ["#PCLN", "priceline.com"],
"Perrigo Company": ["#PRGO", "Perrigo"],
"QUALCOMM Incorporated": ["#QCOM", "QUALCOMM"],
"Research in Motion Limited": ["#RIMM", "Research in Motion", "RIM", "R.I.M."],
"Ross Stores, Inc.": ["#ROST", "Ross Stores"],
"SanDisk Corporation": ["#SNDK", "SanDisk"],
"Seagate Technology.": ["#STX", "Seagate"],
"Sears Holdings Corporation": ["#SHLD", "Sears"],
"Sigma-Aldrich Corporation": ["#SIAL", "Sigma-Aldrich"],
"Sirius XM Radio Inc.": ["#SIRI"],
"Staples, Inc.": ["#SPLS", "Staples"],
"Starbucks Corporation": ["#SBUX", "Starbucks"],
"Stericycle, Inc.": ["#SRCL", "Stericycle"],
"Symantec Corporation": ["#SYMC", "Symantec"],
"Texas Instruments Incorporated": ["#TXN", "Texas Instruments"],
"VeriSign, Inc.": ["#VRSN", "VeriSign"],
"Vertex Pharmaceuticals Incorporated": ["#VRTX", "Vertex Pharmaceuticals"],
"Viacom Inc.  ": ["#VIAB", "Viacom"],
"Virgin Media Inc.": ["#VMED", "Virgin Media"],
"Vodafone Group Plc": ["#VOD", "Vodafone"],
"Warner Chilcott plc": ["#WCRX", "Warner"],
"Whole Foods Market, Inc.": ["#WFM", "Whole Foods Market"],
"Wynn Resorts, Limited": ["#WYNN", "Wynn Resorts"],
"Xilinx, Inc.": ["#XLNX", "Xilinx"],
"Yahoo! Inc.": ["#YHOO", "Yahoo", "yahoo.com"],
}


class CustomStreamListener(tweepy.StreamListener):
	"""Extend tweepy.StreamListener. Ignore everything but successfull responses.
	Store successfull responses in CouchDB.
	"""

	def handle_tweet(self, tweet):
		"""Iterate companies and store the tweet for each company mentioned in the tweet."""
		for company in COMPANIES:
			for keyword in COMPANIES[company]:
				if keyword in tweet:
					store.store_tweet(tweet, company)
					break # go to next company

	def on_status(self, status):
		"""Called upon successfull retrieval of tweet."""
		self.handle_tweet(status.text)
		# print status.text
	
	def on_error(self, status_code):
		"""Called upon failed request. This will be ignored to keep the stream alive."""
		# print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
		"""Called upon timed out request. This will be ignored to keep the stream alive."""
		# print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

def collect(keywords=COMPANIES):
	"""
	Start the stream collection.

	Keyword arguments:
    keywords -- the list of words to use in the stream filtering (default COMPANIES)

	"""
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
	sapi.filter(track=keywords)

def get_companies_and_stock_symbols():
	return [(c, COMPANIES[c][0]) for c in COMPANIES]





