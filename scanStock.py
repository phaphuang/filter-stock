# -*- coding: utf-8 -*-
# encode for read Thai character
#from __future__ import unicode_literals
#import sys
#import importlib
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

import pandas as pd
import numpy as np


def scan_stock():
    file_name = 'Stock_2017.xlsx'
    
    fs = pd.read_excel('raw/' + file_name, encoding='utf-8', skiprows=2, dtype=object).T
    
    year = int(file_name.split('_')[1].split('.')[0])
    print(year)

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
    fs['index'] = fs['index'].apply(lambda x: x.split(' (')[0])
    fs = fs.set_index(['index','Year'])
    fs = fs.T
    fs.rename(columns={' ROE': 'ROE', 'Interest Bearing Debt to Total Equity': 'Debt to Total Equity'}, inplace=True)

    #print(fs.columns[79][0])
    #print(fs['Debt to Total Equity'])
    
    ### Convert n.a. string to NaN value
    fs = fs.replace('n.a.', np.nan)
    #print(fs['ROE'].iloc[:,-1])
    
    avgROE = (fs['ROE'].iloc[:,-1]+fs['ROE'].iloc[:,-2]+fs['ROE'].iloc[:,-3]) / 3
    avgNPM = (fs['Net Profit Margin'].iloc[:,-1]+fs['Net Profit Margin'].iloc[:,-2]+fs['Net Profit Margin'].iloc[:,-3]) / 3
    avgDE = (fs['Debt to Total Equity'].iloc[:,-1]+fs['Debt to Total Equity'].iloc[:,-2]+fs['Debt to Total Equity'].iloc[:,-3]) / 3
    growth = ((fs['EPS'].iloc[:,-1] > fs['EPS'].iloc[:,-2]) & (fs['EPS'].iloc[:,-2] > fs['EPS'].iloc[:,-3]))
              #  & (fs['EPS'].iloc[:,-3] > fs['EPS'].iloc[:,-4]) & (fs['EPS'].iloc[:,-4] > fs['EPS'].iloc[:,-5]))
    #print(avgNPM)

    filterStock = fs[(fs['EPS'][year] > fs['EPS'][year-1]) &
       (fs['EPS'][year-1] > fs['EPS'][year-2]) &
       (((fs['ROE'][year]+fs['ROE'][year-1]+fs['ROE'][year-2])/3) > 15)]['Stock Name']
    #print(filterStock)

    findStock = fs[(avgROE > 15) & (avgNPM > 0.05) & (avgDE < 1.0) & (growth == True)]
    #print(findStock.iloc[:,0])
    #print(findStock.count())

    return findStock.iloc[:, 0], fs

result, prod_df = scan_stock()
print(result.count())
print(result)
