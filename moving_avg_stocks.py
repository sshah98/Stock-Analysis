import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

style.use('ggplot')

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2017, 12, 31)

df = web.DataReader('TSLA', "yahoo", start, end)
# df.to_csv('TSLA.csv')

df = pd.read_csv('TSLA.csv', parse_dates=True, index_col=0)

df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
print(df.head())

ax1 = plt.subplot2grid((6,1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()

#df[['High', 'Low']].plot()
#plt.show()
