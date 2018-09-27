from scanStock import scan_stock
from stockValuation_no10 import valuation_stock

import datetime as dt
import pandas as pd
import fix_yahoo_finance as yf
#import pandas_datareader.data as web

# Create CSV file
start = "2000-1-1"
end = "2017-7-14"

"""
stock_list = []
for stock in scan_stock():
    #print(stock + '.BK')
    if stock not in ("M-CHAI", "PS", "SMG"):
        df = web.DataReader((stock + '.BK'), 'yahoo', start, end)
        try:
            if (df.ix['2017-02-07'].Close) < valuation_stock(stock):
                #print(stock)
                stock_list.append(stock)
        except RemoteDataError:
            print("Data does not exist!")

#print(stock_list)
#df = web.DataReader('M-CHAI.BK', 'yahoo', start, end)
#print(df.ix['2017-02-07'].Close)
"""

stock_list = []
priceavg_list = []
for stock in scan_stock():
    #print(stock + '.BK')
    if stock not in ("M-CHAI", "PS", "SMG"):
        df = yf.download(stock + '.BK', start=start, end=end)
        price_avg, price_table = valuation_stock(stock)
        try:
            if (df.ix[end].Close) < price_avg:
                #print(stock)
                stock_list.append(stock)
                priceavg_list.append(price_avg)
        except:
            print("Data does not exist!")


sl = pd.DataFrame({'Stock': stock_list, 'Price': priceavg_list})
sl.to_csv('raw/Stock_List.csv')
#print(sl)
