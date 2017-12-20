import quandl
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
from statistics import mean


style.use('ggplot')

start = dt.datetime(2000,1,1)
end = dt.datetime.today()
df = web.DataReader('TSLA', 'google', start, end)

df_ohlc = df['Close'].resample('10D').ohlc()
df_ohlc = df_ohlc.reset_index()
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

x = np.array(df_ohlc['Date'], dtype=np.float64)
y = np.array(df_ohlc['close'], dtype=np.float64)

def best_fit_slope_and_intercept(x,y):
    m = (((mean(x) * mean(y)) - mean(x * y)) /
         ((mean(x) ** 2) - mean(x ** 2)))

    b = mean(y) - m*mean(x)

    return m, b

m,b = best_fit_slope_and_intercept(x, y)
# print(m,b)



df_ohlc['close'].plot()
plt.show()
# print(df_ohlc.head())