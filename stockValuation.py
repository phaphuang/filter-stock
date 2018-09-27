import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fs = pd.read_excel('raw/Stockscreen and Valuation 2015.xlsx', encoding='utf-8', skiprows=2, sheetname="Financial Ratio").T

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

val = pd.read_excel('raw/Stockscreen and Valuation 2015.xlsx', encoding='utf-8', skiprows=2, sheetname="Valuation").T
#print(val)
val = val.rename(columns={0:'Year'})
val = val.reset_index()

val['index'] = val['index'].apply(lambda x: replace_nan(x))
val['index'] = val['index'].fillna(method='ffill')
val['index'][0] = 'Stock Name'
val['index'] = val['index'].apply(lambda x: x.split(', ')[-1])
val = val.set_index(['index','Year'])
val = val.T

# Valuation Stock
stock_name = 'PM'
# 1) Find K value (Percent)
Rf = 4.0
Rm = 12.0
beta = val[val['Stock Name'].iloc[:, 0] == stock_name]['Beta']['3 Yr']    #['Beta']['3 Yr'].dropna()
beta = beta[beta != 'n.a.']
print('Beta: {}'.format(beta.iloc[0]))
#print(beta.isnull().values.any())
K = (Rf + (Rm - Rf) * beta) / 100
print('K (%): {}'.format(K.iloc[0]*100))

# 2) Find g value (Percent)
ROE = fs[fs['Stock Name'].iloc[:, 0] == stock_name]['ROE (%)'].iloc[:, -1].iloc[0] / 100    #(fs['ROE (%)'][2013] + fs['ROE (%)'][2014] + fs['ROE (%)'][2015]) / 3
payout = val[val['Stock Name'].iloc[:, 0] == stock_name]['Payout Ratio (%)'].iloc[:, -2].iloc[0] / 100   #(val['Payout Ratio (%)'][2013] + val['Payout Ratio (%)'][2014] + val['Payout Ratio (%)'][2015]) / 3
print('ROE (%): {}\nPayout Ratio (%): {}'.format(ROE*100, payout*100))
g = ROE * (1 - payout)
print('g (%): {}'.format(g*100))

# 3) Find Target Price by Dividend Discount Model(DDM)
dividendYield = val[val['Stock Name'].iloc[:, 0] == stock_name]['DPS (Baht per share)'].iloc[:, -1].iloc[0]
target_price_dy = dividendYield * (1 + g) / (K - g)
print('Dividend Yield: {}\nPrice by DDM: {}'.format(dividendYield, target_price_dy.iloc[0]))
percent = [0.03, 0.05, 0.07, 0.10]
target_price_g = [dividendYield * (1 + p) / (K - p) for p in percent]
print('Price by g=3%: {}\nPrice by g=5%: {}\nPrice by g=7%: {}\nPrice by g=10%: {}'
            .format(target_price_g[0].iloc[0], target_price_g[1].iloc[0], target_price_g[2].iloc[0], target_price_g[3].iloc[0]))

# 4) Find Target Price by Price per Equity (P/E)
EPS = fs[fs['Stock Name'].iloc[:, 0] == stock_name]['EPS (Baht per share)'].iloc[:, -1].iloc[0]
print('Earning Per Share: {}'.format(EPS))
target_pe = payout / (K - g)
target_price_pe = target_pe * (EPS * (1 + g))
print('Target PE: {}\nPrice by PE: {}'.format(target_pe.iloc[0], target_price_pe.iloc[0]))
maxPE = val[val['Stock Name'].iloc[:, 0] == stock_name]['Max P/E'].iloc[0].iloc[0]
maxPE_price = maxPE * (EPS) * (1 + percent[0])
avgPE = val[val['Stock Name'].iloc[:, 0] == stock_name]['Average P/E'].iloc[0].iloc[0]
avgPE_price = avgPE * (EPS) * (1 + percent[0])
minPE = val[val['Stock Name'].iloc[:, 0] == stock_name]['Min P/E'].iloc[0].iloc[0]
minPE_price = minPE * (EPS) * (1 + percent[0])
print('Max P/E: {}\nPrice by MaxPE: {}\nAverage P/E: {}\nPrice by AvgPE: {}\nMin P/E: {}\nPrice by MinPE: {}'
            .format(maxPE, maxPE_price, avgPE, avgPE_price, minPE, minPE_price))
target_pe_g = [payout / (K - p) for p in percent]
print('P/E by g=3%: {}\nP/E by g=5%: {}\nP/E by g=7%: {}\nP/E by g=10%: {}'
            .format(target_pe_g[0].iloc[0], target_pe_g[1].iloc[0], target_pe_g[2].iloc[0], target_pe_g[3].iloc[0]))
target_price_pe_g = [EPS * (1 + p) * t for t, p in zip(target_pe_g, percent)]
print('Price by P/E g=3%: {}\nPrice by P/E g=5%: {}\nPrice by P/E g=7%: {}\nPrice by P/E g=10%: {}'
            .format(target_price_pe_g[0].iloc[0], target_price_pe_g[1].iloc[0], target_price_pe_g[2].iloc[0], target_price_pe_g[3].iloc[0]))

# 5) Find Price Target from Price/Book Value
BV = val[val['Stock Name'].iloc[:, 0] == stock_name]['Book value'].iloc[:, -1].iloc[0]
print('Book Value: {}'.format(BV))
target_bv = (ROE - g) / (K - g)
target_price_bv = target_bv * (BV * (1 + g))
print('Target BV: {}\nPrice by BV: {}'.format(target_bv.iloc[0], target_price_bv.iloc[0]))
maxBV = val[val['Stock Name'].iloc[:, 0] == stock_name]['Max P/BV'].iloc[0].iloc[0]
maxBV_price = maxBV * (BV) * (1 + percent[0])
avgBV = val[val['Stock Name'].iloc[:, 0] == stock_name]['P/BV'].iloc[0].iloc[0]
avgBV_price = avgBV * (BV) * (1 + percent[0])
minBV = val[val['Stock Name'].iloc[:, 0] == stock_name]['Min P/BV'].iloc[0].iloc[0]
minBV_price = minBV * (BV) * (1 + percent[0])
print('Max B/V: {}\nPrice by MaxBV: {}\nAverage B/V: {}\nPrice by AvgBV: {}\nMin B/V: {}\nPrice by MinBV: {}'
            .format(maxBV, maxBV_price, avgBV, avgBV_price, minBV, minBV_price))
target_bv_g = [(ROE - p) / (K - p) for p in percent]
print('P/BV by g=3%: {}\nP/BV by g=5%: {}\nP/BV by g=7%: {}\nP/BV by g=10%: {}'
            .format(target_bv_g[0].iloc[0], target_bv_g[1].iloc[0], target_bv_g[2].iloc[0], target_bv_g[3].iloc[0]))
target_price_bv_g = [t * BV * (1 + p) for t, p in zip(target_bv_g, percent)]
print('Price by P/BV g=3%: {}\nPrice by P/BV g=5%: {}\nPrice by P/BV g=7%: {}\nPrice by P/BV g=10%: {}'
            .format(target_price_bv_g[0].iloc[0], target_price_bv_g[1].iloc[0], target_price_bv_g[2].iloc[0], target_price_bv_g[3].iloc[0]))

data = {'Detail': ['Price by Dividend Discount Model', 'Price by g=3%', 'Price by g=5%', 'Price by g=7%', 'Price by g=10%',
                   'Price by PE = %.2f' % target_pe.iloc[0], 'Price by MaxPE', 'Price by AvgPE', 'Price by MinPE',
                   'Price by P/E g=3%', 'Price by P/E g=5%', 'Price by P/E g=7%', 'Price by P/E g=10%',
                   'Price by BV = %.2f' % target_bv.iloc[0], 'Price by MaxBV', 'Price by AvgBV', 'Price by MinBV',
                   'Price by P/BV g=3%', 'Price by P/BV g=5%', 'Price by P/BV g=7%', 'Price by P/BV g=10%'
        ],
        'Price': [target_price_dy.iloc[0], target_price_g[0].iloc[0], target_price_g[1].iloc[0], target_price_g[2].iloc[0], target_price_g[3].iloc[0],
                  target_price_pe.iloc[0], maxPE_price, avgPE_price, minPE_price,
                  target_price_pe_g[0].iloc[0], target_price_pe_g[1].iloc[0], target_price_pe_g[2].iloc[0], target_price_pe_g[3].iloc[0],
                  target_price_bv.iloc[0], maxBV_price, avgBV_price, minBV_price,
                  target_price_bv_g[0].iloc[0], target_price_bv_g[1].iloc[0], target_price_bv_g[2].iloc[0], target_price_bv_g[3].iloc[0]
        ]
}

price_table = pd.DataFrame(data)
#price_table.reset_index(inplace=True)
#price_table = price_table.set_index(price_table['Detail'])
print(price_table)

#k_means = KMeans(n_clusters=2)
#y_pred = k_means.fit_predict(price_table['Price'])

#price_avg = price_table['Price'].mean()
price_avg = (abs(price_table['Price'].max()) - abs(price_table['Price'].min())) / 2
print(price_avg)

plt.scatter(price_table.index, price_table['Price'])
for i, txt in enumerate(price_table['Detail']):
    plt.annotate(txt, (price_table.index[i], price_table['Price'][i]))
plt.show()
