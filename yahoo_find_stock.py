# -*- coding: utf-8 -*-
"""
Created on Fri May 12 23:54:33 2017

@author: Aniwat
"""

import csv
import pandas_datareader.data as data
from pandas_datareader.yahoo.quotes import _yahoo_codes

stocklist = ['advanc.bk']

#http://www.jarloo.com/yahoo_finance/
#https://greenido.wordpress.com/2009/12/22/yahoo-finance-hidden-api/
_yahoo_codes.update({'Market Cap': 'j1'})
_yahoo_codes.update({'Div Yield': 'y'})
_yahoo_codes.update({'Bid': 'b'})
_yahoo_codes.update({'Ask': 'a'})
_yahoo_codes.update({'Prev Close': 'p'})
_yahoo_codes.update({'Open': 'o'})
_yahoo_codes.update({'1 yr Target Price': 't8'})
_yahoo_codes.update({'Earnings/Share': 'e'})
_yahoo_codes.update({"Day’s Range": 'm'})
_yahoo_codes.update({'52-week Range': 'w'})
_yahoo_codes.update({'Volume': 'v'})
_yahoo_codes.update({'Avg Daily Volume': 'a2'})
_yahoo_codes.update({'EPS Est Current Year': 'e7'})
_yahoo_codes.update({'EPS Est Next Quarter': 'e9'})

data.get_quote_yahoo(stocklist).to_csv('test.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

data.get_quote_yahoo(stocklist).transpose()

print(data.get_quote_yahoo(stocklist).transpose())