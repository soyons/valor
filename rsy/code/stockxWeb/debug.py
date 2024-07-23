import pymongo
import pandas as pd 
from dateutil.parser import parse 
import pytz 

def to_utc8(dt):
    # 将原始时间设置为UTC时区
    dt = dt.replace(tzinfo=pytz.utc)
    # 转换为东八区的时间
    dt = dt.astimezone(pytz.timezone('Asia/Shanghai'))
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

if __name__ == '__main__':
    client = pymongo.MongoClient("localhost", 27017)
    db = client['debug']
    collection = db['stockx']
    data = pd.DataFrame(list(collection.find()))
    data['salesNum'] = data['salesVolume'].apply(len)
    data['oldest_time'], data['latest_time'] = zip(*data['salesVolume'].apply(get_time_range))
    print("done")
