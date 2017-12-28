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

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

print(df_ohlc.head())