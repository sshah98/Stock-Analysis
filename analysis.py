import pandas as pd

stock = 'AAPL'

df = pd.read_csv('balancesheet/{0}.csv'.format(stock))

print(df)