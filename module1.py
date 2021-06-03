#module 1
#create by Sergey Tokarev nonnisnon@gmail.com
import yfinance as yf

from settings import list_company
from sqlalchemy import create_engine

engine = create_engine('sqlite:///ticker.db')

def post_data_in_db(ticker):

    msft = yf.Ticker(ticker)
    # get historical market data
    hist = msft.history(period="max")
    try:
        hist.to_sql(name=f'{ticker}.db',
                    con=engine,
                    schema=None,
                    if_exists='fail',
                    index=True, index_label=None, chunksize=None, dtype=None, method=None)
        return print('add')
    except ValueError:
        print('data alredy in db')

for ticker in list_company:
    post_data_in_db(ticker)
