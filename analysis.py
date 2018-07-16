import pandas as pd

from stock_data import download_quotes
from stock_data import acquire_ms_data


symbol = input('Enter the symbol: ')
print("--------------------------------------------------")
print("Downloading {0} to {0}.csv".format(symbol))
try:
    download_quotes(symbol)
    acquire_ms_data(symbol)
except KeyError:
    print("Please enter a correct ticker...")
    
print("--------------------------------------------------")

# df = pd.read_csv('balancesheet/{0}.csv'.format(stock))

# print(df)