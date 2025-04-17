from pymongo import MongoClient
import datetime
from datetime import datetime as dt
import pandas as pd
import time
myclient = MongoClient("mongodb://localhost:27017/")

from collections import OrderedDict
db=myclient["News_Sentiment"]


#a=col.count_documents({'stock.stock_name':'万华化'})
#print(a)
def update_doc(time_stamp,name,label1,label2):
    global db
    year=datetime.datetime.fromtimestamp(time_stamp).year
    print(year)
    col = db[str(year)]
    col.update({'time_stamp':int(time_stamp),"stock.stock_name":name},{"$set":{'label':label1,'label2':label2}},upsert=False,multi=True)

def condition_bankuai(name):
    global db
    for result in db.bankuai.find({'name':name}):
        code_list=result['code_list']
    return code_list

def query_normal(previous_pd,year,skip_num,limit_num):
    global db
    no_more_data = False
    #year=dt.today().year
    col=db[str(year)]
    if previous_pd==None:
        previous_pd=pd.DataFrame()
    else:
        previous_pd = pd.DataFrame(previous_pd)
    result=col.find().sort("time_stamp",-1).limit(limit_num).skip(skip_num)
    data,num=reslut_to_pd(result)
    data=pd.concat([previous_pd,data],ignore_index=True)
    if num<limit_num:
        if num==0:
            no_more_data=True
        year=year-1
        skip_num = -60

    return data,year,skip_num,no_more_data

def query_condition(previous_pd,year,skip_num,limit_num,condition):
    global db
    no_more_data=False
    # year=dt.today().year
    col = db[str(year)]
    if previous_pd == None:
        previous_pd = pd.DataFrame()
    else:
        previous_pd = pd.DataFrame(previous_pd)
    result = col.find(condition).sort("time_stamp", -1).limit(limit_num).skip(skip_num)
    data, num = reslut_to_pd(result)
    data = pd.concat([previous_pd, data], ignore_index=True)
    if num < limit_num:
        if num==0:
            no_more_data=True
        year = year - 1
        skip_num= -60

    return data, year,skip_num,no_more_data

def get_condition(month,day,name,code,SW1,SW2,SW3,bk_name):
    condition={}
    if month!= None:
        condition["time.month"]=month
    if day!=None:
        condition["time.day"]=day
    if name!="":
        condition["stock.stock_name"]={'$regex':name}
    if code!="":
        condition["stock.stock_code"]=code
    if SW1!=None:
        condition["stock.SW1"] = SW1
    if SW2!=None:
        condition["stock.SW2"] = SW2
    if SW3!=None:
        condition["stock.SW3"] = SW3
    if bk_name!=None:
        code_list=condition_bankuai(bk_name)
        condition['stock.stock_code']={'$in':code_list}


    return condition




def reslut_to_pd(result):
    num=0
    row_list=[]

    df=pd.DataFrame()
    for data in result:
        num+=1
        news = OrderedDict()
        news['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['time_stamp']))
        news['content'] = data['content']
        news["class"] = data["class"]
        news["score"] = data["score"]
        if len(data["stock"])>1:
            name=''
            code=''
            for i in range(len(data['stock'])):
                name=name+data["stock"][i]["stock_name"]+', '
                code=code+data["stock"][i]["stock_code"]+', '
            news["stock_name"]=name
            news["stock_code"]=code
        else:
            news["stock_name"] = data["stock"][0]["stock_name"]
            news["stock_code"] = data["stock"][0]["stock_code"]
        news["label"] = data["label"]
        news["label2"] = data["label2"]
        news['time_stamp'] = data['time_stamp']
        row_list.append(news)
    df = pd.DataFrame(row_list)

    return df,num




db_wx=myclient['wx_public']
def query_wx(previous_pd,skip_num,limit_num):
    global db_wx
    name_list=db_wx.list_collection_names()
    no_more_data = False
    #year=dt.today().year
    #print(public_name)

    if previous_pd==None:
        previous_pd=pd.DataFrame()
    else:
        previous_pd = pd.DataFrame(previous_pd)
    data_all=pd.DataFrame([])
    for name in name_list:
        col = db_wx[name]
        result=col.find().sort("date_num",-1).limit(limit_num).skip(skip_num)
        data,num=reslut_to_pd_wx(result)
        data_all=pd.concat([data,data_all],ignore_index=True)
    #print(data)
    data_all=data_all.sort_values("date_num",ascending=False)
    data_all=pd.concat([previous_pd,data_all],ignore_index=True)


    if num<limit_num:
        no_more_data=True

    return data_all,no_more_data

def reslut_to_pd_wx(result):
    num=0
    row_list=[]
    #print('开始转换')
    #df=pd.DataFrame()
    for data in result:

        num+=1
        news = OrderedDict()
        news['date'] = data['date']
        news['title'] = '['+data['title']+']'+ '(' + str(data["url"]) + ')'
        news['account']=data['account']
        news["date_num"] = data["date_num"]
        #print(data["url"])
        row_list.append(news)

    df = pd.DataFrame(row_list)

    return df,num



def query_by_stock():
    return



def query_by_industry():

    return

def query_by_bankuai():
    return