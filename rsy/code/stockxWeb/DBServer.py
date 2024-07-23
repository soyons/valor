import pandas as pd 
from dateutil.parser import parse 
import pytz 
from config import * 
from datetime import datetime, timedelta
from loguru import logger
import threading
import time 
import re 
import pymysql 
from tqdm import tqdm 

local_tz = pytz.timezone('Asia/Shanghai')

def to_utc8(dt):
    # 将原始时间设置为UTC时区
    dt = dt.replace(tzinfo=pytz.utc)
    # 转换为东八区的时间
    dt = dt.astimezone(local_tz)
    return dt

def get_time_range(sales):
    # 初始化最早和最晚的时间
    oldest_time = parse('9999-12-31T23:59:59Z')
    latest_time = parse('0001-01-01T00:00:00Z')

    # parse date 
    for sale in sales:
        if isinstance(sale, list):
            continue
        time = parse(sale['time'])
        if time < oldest_time:
            oldest_time = time 
        if time > latest_time:
            latest_time = time 
    return to_utc8(oldest_time), to_utc8(latest_time)

def count_sales_in_time_range(df:pd.DataFrame, time_range:int, res:dict):
    end_time = datetime.now()
    start_time = end_time - timedelta(time_range)
        
    item_template = {
        f'latest_{time_range}days_count': 0,
        f'latest_{time_range}days_lowPrice': 1000000,
        f'latest_{time_range}days_highPrice': 0,
        f'latest_{time_range}days_count_expr': 0,
        f'latest_{time_range}days_lowPrice_expr': 1000000,
        f'latest_{time_range}days_highPrice_expr': 0
    }

    for row in tqdm(df.iterrows()):
        row = row[1]
        sku = row['sku']
        if sku not in res:
            res[sku] = dict()
            res[sku]['sku'] = sku
            res[sku]['shoeName'] = row['shoename']
            res[sku]['salesNum'] = 0
            item = res[sku]
        else:
            item = res[sku]
        if f'latest_{time_range}days_count' not in item:
            for key, value in item_template.items():
                item[key] = value

        # 全部销量的统计
        date = row['time']
        if start_time < date <= end_time:
            price = int(re.search(r"\d+", row['price']).group(0))
            if price < item[f'latest_{time_range}days_lowPrice']:
                item[f'latest_{time_range}days_lowPrice']= price
            if price > item[f'latest_{time_range}days_highPrice']:
                item[f'latest_{time_range}days_highPrice'] = price 
            
            if row['ordertype'] == 'EXPRESS':
                item[f'latest_{time_range}days_count_expr'] += 1
                if price < item[f'latest_{time_range}days_lowPrice_expr']:
                    item[f'latest_{time_range}days_lowPrice_expr'] = price
                if price > item[f'latest_{time_range}days_highPrice_expr']:
                    item[f'latest_{time_range}days_highPrice_expr'] = price 
                    
            item[f'latest_{time_range}days_count'] += 1 
            item['salesNum'] += 1

class dbServer:
    def __init__(self, refresh_interval = 12 * 3600) -> None:
        self.conn = pymysql.connect(
            host=DBHOST,
            port=DBPORT,
            user=DBUSER,
            password=DBPASSWORD,
            db=DBDATABASE,
            charset='utf8'
        )
        self.last_update = datetime.now()
        self._cache_data, self._cache_ori_data =  self._fetch_data()

        # 异步初始_cache_data 
        self._refresh_interval = refresh_interval
        self._lock = threading.Lock()
        self._data_thread = threading.Thread(target=self._data_thread_init, daemon=True)
        self._data_thread.start()

    def __del__(self):
        self.conn.close()

    def _fetch_data(self):
        logger.info("Fetching data from mysql...")
        # data = pd.DataFrame(list(self.collection.find(
        #     {"SKU": "ID5103"}
        # ))) 
        cur = self.conn.cursor()
        try:
            date_30_days_ago = datetime.now() - timedelta(days=30)
            template = """
                SELECT sku, shoename, size, price, ordertype, time FROM saleData 
                WHERE time > %s
            """
            cur.execute(template, (date_30_days_ago,))
            result = cur.fetchall()
            df_ = pd.DataFrame(result, columns=["sku", "shoename", "size", "price", "ordertype", "time"])
        finally:
            cur.close()
        res = dict()

        count_sales_in_time_range(df_, 3, res)        
        count_sales_in_time_range(df_, 7, res)
        count_sales_in_time_range(df_, 30, res)
        
        data = []
        for _, value in res.items():
            data.append(value)
        df = pd.DataFrame(data)
        return df, df_

    def _data_thread_init(self):
        cur_time = datetime.now()
        if (cur_time - self.last_update).total_seconds() >= self._refresh_interval:
            data = self._fetch_data()
            with self._lock:
                self.last_update = cur_time
                self._cache_data = data 
        time.sleep(self._refresh_interval)
            

    @property
    def data(self) -> pd.DataFrame:
        return self._cache_data
    
    @property
    def ori_data(self) -> pd.DataFrame:
        return self._cache_ori_data

    def find_by_sku(self, sku):
        # if not exists return None 
        cur = self.conn.cursor()
        template = """
        SELECT sku, shoename, size, price, ordertype, time FROM saleData WHERE sku=%s
        """
        try:
            cur.execute(template, (sku, ))
            result = cur.fetchall()
        finally:
            cur.close()
        return result 
    
    def find_by_shoeName(self, shoename):
        cur = self.conn.cursor()
        template = """
        SELECT sku, shoename, size, price, ordertype, time FROM saleData WHERE shoename=%s
        """
        try:
            cur.execute(template, (shoename, ))
            result = cur.fetchall()
        finally:
            cur.close()
        return result  
        
