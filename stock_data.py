import re
import sys
import time
import datetime
import requests
import csv
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import urlretrieve


BALANCESHEET_DIR = 'balancesheet/'
CASHFLOW_DIR = 'cashflow/'
HISTORICAL_DATA_DIR = 'historical_data/'
INCOMESTATEMENT_DIR = 'incomestatement/'
KEYRATIO_DIR = 'keyratio/'
YAHOO_INFO_DIR = 'news/'


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_cookie_value(r):
    return {'B': r.cookies['B']}


def get_page_data(symbol):
    print("[INFO] Getting webpage data...")
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
    print("[INFO] Did not find CrumbStore")


def split_crumb_store(v):
    return v.split(':')[2].strip('"')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


def get_data(symbol, start_date, end_date, cookie, crumb):
    assure_path_exists(HISTORICAL_DATA_DIR)
    filename = 'historical_data/{0}.csv'.format(symbol)
    print("[INFO] Getting historical stock data...")
    url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}".format(
        symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


def get_news(symbol, cookie, crumb):
    assure_path_exists(YAHOO_INFO_DIR)
    filename = 'news/{0}.csv'.format(symbol)
    print("[INFO] Getting news of stock...")
    url = "https://finance.yahoo.com/quote/{0}/?p={0}&crumb={1}".format(
        symbol, crumb)
    response = requests.get(url, cookies=cookie)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    mydivs = soup.find_all("div", {"id": "quoteNewsStream-0-Stream"})

    text = mydivs[0].get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    with open(filename, 'w') as handle:
        handle.write(text)


def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())


def download_quotes(symbol):
    start_date = 0
    end_date = get_now_epoch()
    cookie, crumb = get_cookie_crumb(symbol)
    print("[INFO] Downloading data...")
    get_data(symbol, start_date, end_date, cookie, crumb)
    get_news(symbol, cookie, crumb)


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
    print("[INFO] Making necessary directories")
    assure_path_exists(KEYRATIO_DIR)
    assure_path_exists(BALANCESHEET_DIR)
    assure_path_exists(INCOMESTATEMENT_DIR)
    assure_path_exists(CASHFLOW_DIR)
    output_map = {'kr': ['kr', './keyratio'], 'is': ['fs', './incomestatement'],
                  'bs': ['fs', './balancesheet'], 'cf': ['fs', './cashflow']}

    for qType, fInfo in output_map.items():
        # Path to save
        output_path = os.path.join(fInfo[1], output_name)

        # Build http query
        print("[INFO] Getting data from stock ticker...")
        if fInfo[0] == 'kr':
            url = get_morningstar_url(fInfo[0], t=ticker)
        else:
            url = get_morningstar_url(fInfo[0], t=ticker, reportType=qType,
                                      period=12, dataType='A', order='asc', columnYear=5, number=1)
        # Download & save data
        print("[INFO] Saving data...")
        urlretrieve(url, output_path)