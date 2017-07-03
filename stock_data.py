import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

value = open('/home/suraj/Documents/Programming/quandlapikey.txt', 'r').read()
value = value.rstrip('\n')

quandl.ApiConfig.api_key = '%s' % value

data = quandl.get_table('WIKI/PRICES', ticker='SWI')

df = pd.DataFrame(data)

data = df[['ticker', 'date', 'high', 'low', 'close']].copy()



# fig = plt.figure()
# ax1 = plt.subplot2grid((2,1), (0,0))
# ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)
# data.plot(x='date', y=['high', 'low'], ax=ax1)
# data.plot(x='date', y='close', ax=ax2)
# plt.show()

#
# from zipline.api import order, record, symbol
#
#
# def initialize(context):
#     pass
#
#
# def handle_data(context, data):
#     order(symbol('AAPL'), 10)
#     record(AAPL=data.current(symbol('AAPL'), 'price'))