import pandas as pd
import pandas_datareader.data as web
import datetime

#Look at historical data from past 5 years of each company
start = datetime.datetime(2013, 1, 1)
end = datetime.date.today()

quantum