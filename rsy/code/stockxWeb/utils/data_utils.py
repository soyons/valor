from loguru import logger 
import pandas as pd 
from collections import defaultdict
from datetime import datetime, timedelta
import re 
import numpy as np 

def get_detail_data(dbserver, sku, shoename):
    '''
    :return 返回sku或shoename对应的salesVolume, 并调整了orderType
    '''
    def process_data(item):
        '''贩卖结果通过EXPRESS时显示火箭'''
        if item == 'EXPRESS':
            # item = '🚀'
            item = 'EXPRESS'
        else:
            item= ''
        return item
        
    if sku != "NULL" and sku is not None and sku != "":
        data = dbserver.find_by_sku(sku)
    else:
        data = dbserver.find_by_shoeName(shoename)
    if len(data) == 0:
        logger.error("The search is invalid, sku is {}, shoename is {}".format(sku, shoename))
        return None, None, True 
    sales_data = pd.DataFrame(data, columns=["sku", "shoename", "size", "price", "ordertype", "time"])
    sales_data['ordertype'] = sales_data['ordertype'].apply(process_data)
    sales_data = sales_data.sort_values('time', ascending=False)
    shoename = sales_data.iloc[0]['shoename']
    # TODO 让时间显示更好
    # sales_data['time'] = sales_data['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S %z'))
    return sales_data, shoename, False

def count_detail_data(sales_data: pd.DataFrame):

    def count(df:pd.DataFrame, time_range):
        end_time = datetime.now()
        start_time = end_time - timedelta(time_range)
        res = dict()
        res_expr = dict()
        def _check_data(res: dict, size_:str):
            if size_ not in res:
                res[size_] = dict(
                    count = 0,
                    highest_price = 0,
                    lowest_price = 1000000,
                ) 
            else:
                pass 

        for item in df.iterrows():
            item = item[1]
            size_ = item['size']
            date = item['time']
            if start_time < date <= end_time:
                _check_data(res, size_)
                res[size_]['count'] += 1 
                price = int(re.search(r"\d+", item['price']).group(0))
                if price > res[size_]['highest_price']: res[size_]['highest_price'] = price 
                if price < res[size_]['lowest_price']: res[size_]['lowest_price'] = price
                if item['ordertype'] == 'EXPRESS':
                    _check_data(res_expr, size_)
                    res_expr[size_]['count'] += 1
                    if price > res_expr[size_]['highest_price']: res_expr[size_]['highest_price'] = price 
                    if price < res_expr[size_]['lowest_price']: res_expr[size_]['lowest_price'] = price
        # TODO 因为统一了货币，目前是美元，在main界面有，货币在这里不再添加符号
        return res, res_expr 
    
    latest_3days_res, latest_3days_res_expr   = count(sales_data, 3)
    latest_7days_res, latest_7days_res_expr   = count(sales_data, 7)
    latest_30days_res, latest_30days_res_expr = count(sales_data, 30)

    # 用size做单独一列，时间为新的一列
    res = []
    # one object 
    '''
    dict(
        size:int,
        latest_3days_count:int,
        latest_3days_lowPrice:int,
        latest_3days_highPrice:int,
        ....
    )
    '''
    sizes = set(sales_data['size'])
    def _record(item, latest_data:dict, size_:str, day_index:int, expr=False):
        if expr:
            suffix = '_expr'
        else:
            suffix = ''
        if size_ not in latest_data:
            logger.info("[size_:{}, expr:{}] there is no sales info in the latest_{}days data".format(size_, 'True' if expr else 'False', day_index,))
            item['latest_{}days_count{}'.format(day_index, suffix)] = 0
            item['latest_{}days_lowPrice{}'.format(day_index, suffix)] = '\\'
            item['latest_{}days_highPrice{}'.format(day_index, suffix)] = '\\'
        else:
            item['latest_{}days_count{}'.format(day_index, suffix)] = int(latest_data[size_]['count'])
            item['latest_{}days_lowPrice{}'.format(day_index, suffix)] = latest_data[size_]['lowest_price']
            item['latest_{}days_highPrice{}'.format(day_index, suffix)] = latest_data[size_]['highest_price']
        

    for size_ in sizes:
        item = dict()
        item['size'] = size_ 
        _record(item, latest_3days_res, size_, 3)
        _record(item, latest_7days_res, size_, 7)
        _record(item, latest_30days_res, size_, 30)
        _record(item, latest_3days_res_expr, size_, 3, True)
        _record(item, latest_7days_res_expr, size_, 7, True)
        _record(item, latest_30days_res_expr, size_, 30, True)
        res.append(item)
    df = pd.DataFrame(res)
    df['size_f'] = df['size'].replace(r"\D+", "", regex=True)
    df['size_f'] = df['size_f'].replace('', np.nan, inplace=True)
    df['size_f'] = df['size_f'].astype(float)

    df = df.sort_values('size_f', ascending=True)
    return df
