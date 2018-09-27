import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

# Create CSV file
start = dt.datetime(2000,1,1)
end = dt.datetime(2016,12,31)

df = web.DataReader('BBL.BK', 'yahoo', start, end)
#print(df.head())
df.to_csv('bbl.csv')
