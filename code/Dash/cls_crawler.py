# coding:utf-8
import requests
import time
import pandas as pd
from collections import OrderedDict
from pymongo import MongoClient
import random
import re
import time, datetime
import hashlib
from hashlib import md5




df1 = pd.read_excel("sw.xlsx")

stock_name_list = list(df1["证券名称"])

code_dict = df1.set_index(['证券名称'])['Wind代码'].to_dict()

sw1_name = df1.set_index(['证券名称'])['SW1Name'].to_dict()
sw2_name = df1.set_index(['证券名称'])['SW2Name'].to_dict()
sw3_name = df1.set_index(['证券名称'])['SW3Name'].to_dict()

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["News_Sentiment"]
#mycol = db["2021"]
#col_list = db.list_collection_names()


def find_mentioned_stocks(name_list, text):
    mentioned_stocks = []
    for stock_name in name_list:
        if text.find(stock_name) != -1:
            mentioned_stocks.append(stock_name)
        else:
            continue
    return mentioned_stocks


def get_sentence_by_keywords(text, keyword):
    keyword1 = keyword
    if keyword[0] == "*":
        keyword1 = keyword.replace("*", "", 1)
    condition = '[【 。 ； ]*[^。【 ；]*' + keyword1 + '[^。]*[。]'

    pattern = re.compile(condition)
    sentences = re.findall(pattern, text)
    for i in range(len(sentences)):
        if sentences[i][0] == "。":
            sentences[i] = sentences[i].replace("。", "", 1)
        elif sentences[i][0] == "；":
            sentences[i] = sentences[i].replace("；", "", 1)
    return sentences


def tf_serving_request(text):
    a=[0,1,2]
    y =random.choice(a)

    score = random.random()
    if y == 0:
        class_ = "正向"
    elif y == 2:
        class_ = "负向"
    elif y == 1:
        class_ = "中性"

    return class_, round(score, 5)

def get_time_stamp(date):
    timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

# 为了生成爬虫中的md5 码
def USE_SHA(text):
    if not isinstance(text, bytes):
        text = bytes(text, 'utf-8')
    sha = hashlib.sha1(text)
    encrypts = sha.hexdigest()
    return encrypts
def md5value(s):
    a = md5(s.encode()).hexdigest()
    return a
def get_sign(param):
    b = USE_SHA(param)
    c = md5value(b)
    return c


def clean_text(text):
    text = text.replace("【", "")
    text = text.replace("】", "。")
    text = text.replace(" ", "")
    text = re.sub(r'<[^>]+>', '', text)
    # text = text.replace("<p>", "")
    # text = text.replace("</p>", "")
    return text


def getNewsDetail(item_list,website,end_time):
    global db
    # 财联社和华尔街见闻不同
    if website==1:
        key_name="ctime"
        website_name="财联社"
    elif website==2:
        key_name='display_time'
        website_name="华尔街"

    news_list = []
    for item in item_list:
        news = OrderedDict()
        text = item['content']
        text = clean_text(text)
        time_stamp = item[key_name]
        if time_stamp<end_time:
            break
        name_list = find_mentioned_stocks(stock_name_list, text)
        date_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
        date_ = datetime.datetime.strptime(date_, '%Y-%m-%d %H:%M:%S')
        time_dic = {"year": date_.year, "month": date_.month, "day": date_.day, "hour": date_.hour,
                    "minute": date_.minute, "week": date_.weekday()}
        #mycol = db[str(date_.year)]
        # if str(date_.year) not in col_list:
        #     mycol = db[str(date_.year)]
        #     col_list.append(str(date_.year))
        if len(name_list) == 0:
            # row_list.append({"content":text,"label":5})
            print("处理成功    无关新闻")


        elif len(name_list) == 1:
            # pred,score=predict(text,model)
            stock_name = name_list[0]
            stock_code = code_dict[name_list[0]]
            class_, score = tf_serving_request(text)
            stock = [{"stock_name": stock_name, "stock_code": stock_code, "SW1": sw1_name[stock_name],
                      "SW2": sw2_name[stock_name], "SW3": sw3_name[stock_name]}]
            news["time_stamp"] = time_stamp
            news["time"] = time_dic
            news["content"] = text
            news["class"] = class_
            news["score"] = score
            news["stock"] = stock

            news["label"] = ""
            news["label2"] = ""
            news["website"] = website_name
            try:
                #mycol.insert_one(news)
                news_list.append(news)
                print("数据写入成功")
            except:
                print("失败")


        else:
            all_text = []

            rows = []

            for name in name_list:
                sentences = get_sentence_by_keywords(text, name)
                for sne in sentences:
                    if sne not in all_text:
                        news = OrderedDict()
                        all_text.append(sne)
                        stock = []
                        class_, score = tf_serving_request(sne)
                        # pred,score=predict(sne,model)
                        all_text.append(sne)
                        list_2 = find_mentioned_stocks(stock_name_list, sne)
                        if len(list_2) <= 1:
                            stock = [{"stock_name": name, "stock_code": code_dict[name], "SW1": sw1_name[name],
                                      "SW2": sw2_name[name], "SW3": sw3_name[name]}]
                        else:
                            for name2 in list_2:
                                stock.append(
                                    {"stock_name": name2, "stock_code": code_dict[name2], "SW1": sw1_name[name2],
                                     "SW2": sw2_name[name2], "SW3": sw3_name[name2]})

                        news["time_stamp"] = time_stamp
                        news["time"] = time_dic
                        news["content"] = sne
                        news["class"] = class_
                        news["score"] = score
                        news["stock"] = stock
                        news["label"] = ""
                        news["label2"] = ""
                        news["website"] = website_name
                        rows.append(news)
            try:
                #mycol.insert_many(rows)
                news_list.extend(rows)
                print("数据写入成功2")
            except:
                print("失败2")
    for news in news_list:
        mycol=db[str(news['time']['year'])]
        content_insert=news['content']
        time_stamp_insert=news['time_stamp']
        res = mycol.count_documents({'time_stamp': time_stamp_insert,'content':content_insert})
        if res==0:
            mycol.insert_one(news)
        else:
            continue
    return news_list


# 'https://www.cls.cn/nodeapi/telegraphList?app=CailianpressWeb&category=&lastTime=1610507016&last_time=1610507016&os=web&refresh_type=1&rn=20&sv=7.5.5&sign=7efc797650dadd3bbcfcb47e39f4a2b3'


start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())#'2021-02-01 09:00:59'
#end_time = '2021-02-04 14:10:59'
def get_cls_data(start_time):
    latest_time = get_time_stamp(start_time)
    end_time = latest_time-180 #get_time_stamp(end_time)
    receive_num = 1

    url1 = "https://www.cls.cn/nodeapi/TelegraphList?"
    url2 = 'https://www.cls.cn/v1/roll/get_roll_list?'
    url3 = "https://www.cls.cn/nodeapi/updateTelegraphList?"

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'}
    news_num = 30
    news_list = []
    try:
        while latest_time >= end_time:
            params1 = 'app=CailianpressWeb&category=&lastTime=' + str(latest_time) + '&last_time=' + str(
                latest_time) + '&os=web&refresh_type=1&rn=' + str(receive_num) + '&sv=7.5.5'
            params2 = 'app=CailianpressWeb&category=&lastTime=' + str(latest_time) + '&last_time=' + str(
                latest_time) + '&os=web&refresh_type=1&rn=' + str(receive_num) + '&sv=7.5.5'
            params3 = 'app=CailianpressWeb&category=&hasFirstVipArticle=0&lastTime=' + str(latest_time) + '&os=web&rn=' + str(
                receive_num) + '&subscribedColumnIds=&sv=7.5.5'

            APIurl1 = url1 + params1 + '&sign=' + get_sign(params1)
            APIurl2 = url2 + params2 + '&sign=' + get_sign(params2)
            APIurl3 = url3 + params3 + '&sign=' + get_sign(params3)

            resp = requests.get(APIurl1, headers=headers, verify=True)
            content = resp.json()['data']
            if content["roll_data"] == []:
                resp = requests.get(APIurl2, headers=headers, verify=True)
                content = resp.json()['data']
            latest_time = content["roll_data"][-1]["ctime"]
            news_list.extend(getNewsDetail(content['roll_data'],1,end_time))
        return news_list,False # 判断url是否过期 False 为url正常使用

    except:
        return [],True #表示url过期 需更新






