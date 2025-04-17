from pymongo import MongoClient
import datetime
from datetime import datetime as dt
import pandas as pd
import time
myclient = MongoClient("mongodb://localhost:27017/")
from collections import OrderedDict

db=myclient["wx_public"]
col=db["cls"]
#col.update_many({},{'$set':{'account':"巨潮资讯网"}})

def date2num(date):
    date = date.replace('-', '')

    date = int(date)
    return date
lst=[]
for i in col.find():
    new = OrderedDict()
    new['title'] = i['title']
    new['date']=i['date']
    new['date_num']=i['date']
    new['url'] = i['url']
    new['content']=i['content']
    new['account']=i['account']
    lst.append(new)
df=pd.DataFrame(lst)
df.to_csv("wx_cls_history.csv")
# df=pd.read_csv('wx_hc_history.csv')
# for i in df.index:
#     new=OrderedDict()
#     new['title']=df.loc[i]['title']
#     new['date']=df.loc[i]['date']
#     new['date_num']=date2num(df.loc[i]['date'])
#     new['url'] = df.loc[i]['url']
#     new['content']=df.loc[i]['content']
#     new['account']="华创证券研究"
#     print(new)
#     col.insert_one(new)


#print(date2num('2021-03-01'))

# import os
# src = './QRcode_images'
# files = os.listdir(src)
# files_path = [f'{src}/{file}' for file in files]
# files_path.sort(key=lambda fp: os.path.getctime(fp), reverse=True)
# newest_file = files_path[0]
# print(newest_file)
#
# from mongodb import query_wx
# print(query_wx(None,'azbctx',0,30))