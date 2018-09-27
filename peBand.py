import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import datetime as dt

style.use('ggplot')

gp = pd.read_csv('data/ahc.txt',skiprows=1, names=["Date", "Open", "High", "Low", "Close", "PE"], delim_whitespace=True)
#gp = gp.rename(columns = {'Timestamp': 'Date'})
#gp['Date'] = pd.to_datetime(gp['Date'])

gp['Date'] = gp['Date'].apply(lambda x: dt.datetime.strptime(str(x), '%d/%m/%y'))
gp = gp.set_index(['Date'])
print(gp)
gp['Price'] = gp['Close']
gp['EPS'] = gp['Price'] / gp['PE']

pe_avg = gp['PE'].mean()
pe_std = gp['PE'].std()

pe_avg_plus_1_std = pe_avg + pe_std
pe_avg_plus_2_std = pe_avg + (2 * pe_std)
pe_avg_minus_1_std = pe_avg - pe_std
pe_avg_minus_2_std = pe_avg - (2 * pe_std)

gp['PE+2std'] = pe_avg_plus_2_std * gp['EPS']
gp['PE+1std'] = pe_avg_plus_1_std * gp['EPS']
gp['PEAvg'] = pe_avg * gp['EPS']
gp['PE-1std'] = pe_avg_minus_1_std * gp['EPS']
gp['PE-2std'] = pe_avg_minus_2_std * gp['EPS']

plt.close('all')
fig, ax = plt.subplots(1)
ax.plot(gp.index, gp['Price'])

# rotate and align the tick labels so they look better
fig.autofmt_xdate()

# use a more precise date string for the x axis locations in the toolbar
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.plot(gp.index, gp['PE+2std'], linestyle='--', color='gray')
ax.plot(gp.index, gp['PE+1std'], linestyle='--', color='gray')
ax.plot(gp.index, gp['PEAvg'], linestyle='--', color='gray')
ax.plot(gp.index, gp['PE-1std'], linestyle='--', color='gray')
ax.plot(gp.index, gp['PE-2std'], linestyle='--', color='gray')

#plot.plot(gp.index, gp['Price'])
#plt.plot(gp.index, gp['PE+2std'], linestyle='--', color='gray')
#plt.plot(gp.index, gp['PE+1std'], linestyle='--', color='gray')
#plt.plot(gp.index, gp['PEAvg'], linestyle='--', color='gray')
#plt.plot(gp.index, gp['PE-1std'], linestyle='--', color='gray')
#plt.plot(gp.index, gp['PE-2std'], linestyle='--', color='gray')
plt.show()
