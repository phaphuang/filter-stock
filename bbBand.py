import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

fs = pd.read_excel('raw/Stockscreen and Valuation 2015.xlsx', encoding='utf-8', skiprows=2).T

fs = fs.rename(columns={0:'Year'})
fs = fs.reset_index()

def replace_nan(string):
    if "Unnamed:" in string.split():
        #print('True')
        string = None
    return string

fs['index'] = fs['index'].apply(lambda x: replace_nan(x))
fs['index'] = fs['index'].fillna(method='ffill')
fs['index'][0] = ', Stock Name'
fs['index'] = fs['index'].apply(lambda x: x.split(', ')[-1])
fs = fs.set_index(['index','Year'])
fs = fs.T
fs = fs.rename(columns={' ROE (%)': 'ROE (%)'})

# find individual stock
stock_name = 'BBL'
stock = (fs['Stock Name'] == stock_name)
#print(stock[stock.iloc[:,0] == True].index.values)
col_id = stock[stock.iloc[:,0] == True].index.values


#print(fs['EPS (Baht per share)'].iloc[col_id-1])

df_eps = fs['EPS (Baht per share)'].iloc[col_id-1]
df_eps = df_eps.T
#print(eps)

eps = df_eps[col_id]
plt.plot(df_eps.index, eps)

def bbands(eps, length=30, numsd=1):
    """ returns average, upper band, and lower band"""
    ave = eps.rolling(length, min_periods=0).mean()
    sd = eps.rolling(length, min_periods=0).std()
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)
    return np.round(ave, 3), np.round(upband, 3), np.round(dnband, 3)

df_eps['ave'], df_eps['upper'], df_eps['lower'] = bbands(eps, length=30, numsd=1)
plt.plot(df_eps.index, df_eps['ave'])
plt.plot(df_eps.index, df_eps['upper'])
plt.plot(df_eps.index, df_eps['lower'])
plt.legend()
plt.show()
