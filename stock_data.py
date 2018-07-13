import re
import sys
import time
import datetime
import requests
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import urlretrieve


def get_cookie_value(r):
    return {'B': r.cookies['B']}


def get_page_data(symbol):
    print("Getting webpage data...")
    url = "https://finance.yahoo.com/quote/{0}/?p={0}".format(symbol)
    r = requests.get(url)
    cookie = get_cookie_value(r)
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')


def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")


def split_crumb_store(v):
    return v.split(':')[2].strip('"')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data(symbol, start_date, end_date, cookie, crumb):
    filename = 'historical_data/{0}.csv'.format(symbol)
    print("Getting historical stock data...")
    url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}".format(
        symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())


def download_quotes(symbol):
    start_date = 0
    end_date = get_now_epoch()
    cookie, crumb = get_cookie_crumb(symbol)
    print("Downloading data...")
    get_data(symbol, start_date, end_date, cookie, crumb)


# Encodes morningstar base URL with **params
def get_morningstar_url(fType, **params):
    url_bases = {'kr': "http://financials.morningstar.com/ajax/exportKR2CSV.html?",
                 'fs': "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?"}

    return url_bases[fType] + urlencode(params)


# Downloads morningstar data for a single ticker
def acquire_ms_data(ticker):
    # File name for all data sets
    output_name = ticker + '.csv'

    # Dictionary: Query type, Internal type ref, directory path
    print("Making necessary directories")
    output_map = {'kr': ['kr', './keyratio'], 'is': ['fs', './incomestatement'],
                  'bs': ['fs', './balancesheet'], 'cf': ['fs', './cashflow']}

    for qType, fInfo in output_map.items():
        # Path to save
        output_path = os.path.join(fInfo[1], output_name)

        # Build http query
        print("Getting data from stock ticker...")
        if fInfo[0] == 'kr':
            url = get_morningstar_url(fInfo[0], t=ticker)
        else:
            url = get_morningstar_url(fInfo[0], t=ticker, reportType=qType,
                                      period=12, dataType='A', order='asc', columnYear=5, number=1)
        # Download & save data
        print("Saving data...")
        urlretrieve(url, output_path)


# def get_earnings(symbol):
#
#     url = 'https://www.zacks.com/stock/research/{0}/earnings-announcements'.format(
#         symbol)
#     source = requests.get(url).text
#     soup = BeautifulSoup(source, 'html.parser')
#     table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr(
#         'id') and tag['id'] == "earnings_announcements_earnings_table")
#     print(table)


symbol = input('Enter the symbol: ')
print("--------------------------------------------------")
print("Downloading {0} to {0}.csv".format(symbol))
try:
    download_quotes(symbol)
    acquire_ms_data(symbol)
except KeyError:
    print("Please enter a correct ticker...")
    
print("--------------------------------------------------")
