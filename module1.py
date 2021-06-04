#module 1
#create by Sergey Tokarev nonnisnon@gmail.com
import sqlite3

import yfinance as yf
import sqlite3
from settings import list_company
from sqlalchemy import engine,create_engine

engine = create_engine('sqlite:///ticker.db')


def create_data_from_dframe(ticker):
    """
    get dframe history market data (max) -create db in ticker.db- convert and push pandas dframe to sql
    not upgrade bd new data with this func
    :param ticker: short name of the company symbol
    :return: None, console print
    """
    engine = create_engine('sqlite:///ticker.db')
    data_yf = yf.Ticker(ticker)
    # get historical market data
    hist = data_yf.history(period="max")
    try:
        hist.to_sql(name=f'{ticker}.db',
                    con=engine,
                    schema=None,
                    if_exists='fail',
                    index=True, index_label=None, chunksize=None, dtype=None, method=None)
        return print('add')
    except ValueError:
        return print('data alredy in db')


def post_all_ticker(list_company):
    """

    :param list_company: list symbols (short name of the company symbol)
    :return: None
    """
    for ticker in list_company:
        create_data_from_dframe(ticker)


def upgrade_ticker(ticker):
    """
    get dframe history market data (max) -upgrade [ticker].db in ticker.db
    not use if db not create
    :param ticker: short name of the company symbol
    :return: None
    """

    data_yf = yf.Ticker(ticker)
    # get historical market data
    hist = data_yf.history(period="max")
    con = sqlite3.connect('ticker.db')
    cur = con.cursor()
    max_hist_date=cur.execute(f'''
    SELECT MAX(Date) from [{ticker}.db] ''').fetchall()

    new_data_in_frame = hist.loc[hist.index > max_hist_date[0][0]]
    engine = create_engine('sqlite:///ticker.db')
    new_data_in_frame.to_sql(name=f'{ticker}.db',
            con=engine,
            schema=None,
            if_exists='append',
            index=True, index_label=None, chunksize=None, dtype=None, method=None)


