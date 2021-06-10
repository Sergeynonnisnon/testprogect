import requests
import time
import pandas as pd
from sqlalchemy import create_engine

import sqlite3
ticker = 'MSFT'


def create_new_db(ticker):
    con = sqlite3.connect(f'modulev2.db')
    cur = con.cursor()

    cur.execute(f'''CREATE TABLE IF NOT EXISTS {ticker} (Date DATETIME,Open FLOAT,
    High FLOAT,Low FLOAT,Close FLOAT,Adj_Close FLOAT,Volume BIGINT)''')

    con.commit()
    con.close()



def get_history_data_full(ticker):
    """
    :param ticker:  company name abbreviation string
    :return: pd dataframe
    """
    base_url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'

    params = {'period1': -2208988800, 'period2': int(time.time())}

    params["includePrePost"] = True

    params["interval"] = '1d'
# USE Requests
    response = requests.request(method='GET', url=base_url, params=params)
# parse json
    query = response.json()["chart"]["result"][0]

    timestamps = query["timestamp"]
    ohlc = query["indicators"]["quote"][0]
    volumes = ohlc["volume"]
    opens = ohlc["open"]
    closes = ohlc["close"]
    lows = ohlc["low"]
    highs = ohlc["high"]
    adjclose = closes
    if "adjclose" in query["indicators"]:
        adjclose = query["indicators"]["adjclose"][0]["adjclose"]
# convert to dataframe
    quotes = pd.DataFrame({"Open": opens,
                           "High": highs,
                           "Low": lows,
                           "Close": closes,
                           "Adj Close": adjclose,
                           "Volume": volumes})
    quotes.index = pd.to_datetime(timestamps, unit="s")
    quotes.sort_index(inplace=True)
    return quotes







def frame_to_bd(quotes, ticker):
    """
    append dataframe in db Ticker_mv2.db
    :param quotes: pd.dataframe

    """

    engine = create_engine('sqlite:///Ticker_mv2.db')
    try:
        quotes.to_sql(name=f'{ticker}',
                             con=engine,
                             schema=None,
                             if_exists='fail',
                             index=True, index_label=None, chunksize=None, dtype=None, method=None)
    except ValueError:
        return 'db exist, try upgrade'
get_history_data_full(ticker)