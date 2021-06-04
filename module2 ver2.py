import requests
import time
print(int(time.time()))
import sqlite3
ticker = 'MSFT'
def create_new_db(ticker):
    con = sqlite3.connect(f'modulev2.db')
    cur = con.cursor()

    cur.execute(f'''CREATE TABLE IF NOT EXISTS {ticker} (Date DATETIME,Open FLOAT,
    High FLOAT,Low FLOAT,Close FLOAT,Adj_Close FLOAT,Volume BIGINT)''')

    con.commit()
    con.close()
create_new_db(ticker)


def get_history_data_full(ticker):
    create_new_db(ticker)

    base_url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'

    params = {'period1': -2208988800, 'period2': int(time.time())}

    params["includePrePost"] = True

    params["interval"] = '1d'
    response = requests.request(method='GET', url=base_url, params=params)
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
    data = []
    conn = sqlite3.connect('modulev2.db')
    cur = conn.cursor()

    for i in range(len(timestamps)):


        #data.append((timestamps[i], opens[i], highs[i], lows[i], closes[i], adjclose[i], volumes[i]))

        max_hist_date = cur.execute(f'''INSERT INTO {ticker} VALUES(?,?,?,?,?,?,?)''', (timestamps[i], opens[i], highs[i], lows[i], closes[i], adjclose[i], volumes[i]))
        conn.commit()
    cur.close()
get_history_data_full(ticker)