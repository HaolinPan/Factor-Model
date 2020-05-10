from jqdatasdk import *  #jointquant api
import pymongo
from datetime import datetime
import pandas as pd

auth('13620887713','Pan13620887713')  #login

stocks = get_index_stocks('000300.XSHG') #get HS300 component stocks codes
stockslist = stocks[0:5] #api does not allow request too much in one day

client = pymongo.MongoClient('localhost:27017') #connect to mongoDB

for asset in stockslist:
    #get data from jointquant using api
    data = get_bars(asset,200_000, unit='1m',fields=['date','open','high','low','close','volume'], end_dt='2020-05-09')
    collection = client['AShares'][asset] #creat folder
    collection.create_index([('datetime', pymongo.ASCENDING)], unique=True)
    #save data into database
    for index, row in data.iterrows():
        bar = {}
        bar['open'] = row.open             
        bar['close'] = row.close
        bar['high'] = row.high
        bar['low'] = row.low
        bar['volume'] = row.volume
        bar['datetime'] = row.date
        bar['date'] = bar['datetime'].date().strftime("%Y%m%d")  
        bar['time'] = bar['datetime'].time().strftime("%H:%M:%S") 
        bar['symbol'] = asset             
        flt = {'datetime': bar['datetime']}
        collection.update_one(flt, {'$set':bar}, upsert=True)
    print(asset + 'done!')