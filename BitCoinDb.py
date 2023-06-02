import sqlite3
import datetime

import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import uuid


# conn = sqlite3.connect('resource/bitcoin.db')


class BitCoinFile:
    # conn = sqlite3.connect('resource/bitcoin.db')

    def getTopN(self, limit):
        bitcoin_csv = pd.read_csv("resource/bitcoin.csv").dropna(how='any', axis=0)
        try:
            limit_int = int(limit)
            return bitcoin_csv.head(limit_int).to_dict(orient='records'), 200
        except ValueError:
            return {"Error": "Limit value must be numeric"}, 400

    def getStartAndEnd(self, start, end, dt):
        bitcoin_csv = pd.read_csv("resource/bitcoin.csv").dropna(how='any', axis=0)
        bitcoin_csv['DT'] = pd.to_datetime(bitcoin_csv['Timestamp'], unit='s')

        try:
            format = '%Y-%m-%d'

            if start:
                datetime.datetime.strptime(start, format)
                start_data = bitcoin_csv[bitcoin_csv['DT'] >= start]
                return start_data.head(50).to_dict(orient='records'), 200

            if dt:
                datetime.datetime.strptime(dt, format)
                bitcoin_csv['D'] = pd.to_datetime(bitcoin_csv['Timestamp'], unit='s').dt.strftime('%Y-%m-%d')
                start_data = bitcoin_csv[bitcoin_csv['D'] == dt]
                return start_data.drop(['D'], axis=1).head(50).to_dict(orient='records'), 200

            if end:
                datetime.datetime.strptime(end, format)
                end_data = bitcoin_csv[bitcoin_csv['DT'] <= end]
                return end_data.head(50).to_dict(orient='records'), 200

            if start and end:
                datetime.datetime.strptime(start, format)
                datetime.datetime.strptime(end, format)
                after_start_date = bitcoin_csv["DT"] >= start
                before_end_date = bitcoin_csv["DT"] < end
                between_two_dates = after_start_date & before_end_date
                filtered_dates = bitcoin_csv.loc[between_two_dates]
                return filtered_dates.head(50).to_dict(orient='records'), 200


        except ValueError:
            return {"Error": "Date should be in 'yyyy-mm-dd' format"}, 400

    # bitcoin_csv.to_sql('bitcoin_tbl', conn, if_exists='replace', index=False)

    def insertData(self):
        engine = create_engine('sqlite:///resource/bitcoin.db', echo=True)
        meta = MetaData()
        user = Table(
            'user', meta,
            Column('id', Integer, primary_key=True),
            Column('public_id', Integer),
            Column('name', String),
            Column('password', String)
        )
        meta.create_all(engine)

        ins = user.insert().values(public_id=str(uuid.uuid4()), name='manu', password='manu')
        conn = engine.connect()
        conn.execute(ins)


k = BitCoinFile()
# k.insertData()
