'''
    导出的是最新的50双为csv或者excel格式
'''
import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd 
from config import *
from collections import defaultdict

import pdb
from datetime import datetime, timedelta 
from dateutil import tz 
from dateutil.parser import parse 
import pymysql 

def export(data, time_delta = 3):
    delta_ = datetime.now() - timedelta(days=time_delta)
    df = df[df['time'] > delta_]
    df = data.copy()
    df_express = data[data['ordertype'] == "EXPRESS"]
    return df, df_express

if __name__ == '__main__':
    # data init 
    conn = pymysql.connect(
            host=DBHOST,
            port=DBPORT,
            user=DBUSER,
            password=DBPASSWORD,
            db=DBDATABASE,
            charset='utf8'
        )

    cur = conn.cursor()
    try:
        date_30_days_ago = datetime.now() - timedelta(days=60)
        template = """
            SELECT sku, shoename, size, price, ordertype, time FROM saleData 
            WHERE time > %s
        """
        cur.execute(template, (date_30_days_ago,))
        result = cur.fetchall()
        data = pd.DataFrame(result, columns=["sku", "shoename", "size", "price", "ordertype", "time"])
    finally:
        cur.close()

    df, df_express = export(data)
    with pd.ExcelWriter("stockx_data.xlsx") as writer:
        df_express.to_excel(writer, sheet_name="express data")
        df.to_excel(writer, sheet_name="total data")
