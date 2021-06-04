from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from settings import list_company
from module1 import *
#create by Tokarev Sergey
app = Flask(__name__)
api = Api(app)

db = SQLAlchemy(app)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p> resource not found.</p>", 404


@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')


@app.route('/api/<ticker>', methods=['GET'])
def get_ticker(ticker):
    conn = sqlite3.connect('ticker.db')

    cur = conn.cursor()
    response = cur.execute(f'''SELECT 
		 [Date]
		,[Open]
		,[High]
		,[Low]
		,[Close]
		,[Volume]
		,[Dividends]
		,[Stock Splits]
		FROM [{ticker}.db]''').fetchall()

    conn.commit()
    cur.close()
    return jsonify({ticker: response})


@app.route('/api/get_all', methods=['GET'])
def get_all():
    all_data = {}

    for ticker in list_company:

        conn = sqlite3.connect('ticker.db')

        cur = conn.cursor()
        get_all_data = cur.execute(f'''SELECT *	FROM [{ticker}.db]''').fetchall()
        conn.commit()
        cur.close()
        all_data[ticker] = get_all_data

    return jsonify(all_data)


if __name__ == "__main__":
    app.run(debug=True)
