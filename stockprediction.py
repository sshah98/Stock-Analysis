import bs4 as bs
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data
import pickle
import requests


def sp500_tickers():
    resp = requests.get(
        'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as myfile:
        pickle.dump(tickers, myfile)

    return tickers


def stock_data(reload_sp500=False):

    if reload_sp500:
        tickers = sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as myfile:
            tickers = pickle.load(myfile)

    if not os.path.exists('tickers'):
        os.makedirs('tickers')

    start = dt.datetime(2017, 8, 1)
    end = dt.datetime(2018, 1, 1)

    try:

        for ticker in tickers:
            # just in case your connection breaks, we'd like to save our progress!
            if not os.path.exists('tickers/{}.csv'.format(ticker)):
                df = data.DataReader(ticker, "google", start, end)
                df.to_csv('tickers/{}.csv'.format(ticker))
            else:
                print('Already have {}'.format(ticker))

    except:
        pass


def combine_data():
    with open("sp500tickers.pickle", "rb") as myfile:
        tickers = pickle.load(myfile)

    main_df = pd.DataFrame()
    try:
        for index, ticker in enumerate(tickers):
            df = pd.read_csv('tickers/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)

            # df['{}_HL_pct_diff'.format(ticker)] = (
            #     df['High'] - df['Low']) / df['Low']
            # df['{}_daily_pct_chng'.format(ticker)] = (
            #     df['Close'] - df['Open']) / df['Open']
            
            # df.rename(columns={'Close':ticker}, inplace=True)
            # df.drop(['Open','High','Low','Volume'],1,inplace=True)


            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

            if index % 10 == 0:
                print(index)

            print(main_df.head())
            main_df.to_csv('sp500_joined_closes.csv')

    except:
        pass

combine_data()
