import requests
import time
import pandas as pd
from collections import OrderedDict

import hashlib
from hashlib import md5

'''
财联社 sign
'''

#url='https://www.cls.cn/telegraph'
def get_time_stamp(date):
    timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

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

def getNewsDetail(item_list):
    news_list = []
    for item in item_list:
        news=OrderedDict()
        news['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item['ctime']))
        news['title'] = item['title']
        news['brief'] = item['content']
        news['content'] = item['content']
        news_list.append(news)
    return news_list

#'https://www.cls.cn/nodeapi/telegraphList?app=CailianpressWeb&category=&lastTime=1610507016&last_time=1610507016&os=web&refresh_type=1&rn=20&sv=7.5.5&sign=7efc797650dadd3bbcfcb47e39f4a2b3'
start_time='2021-01-21 09:00:59'

last_time=get_time_stamp(start_time)
receive_num=20
print(last_time)
url1="https://www.cls.cn/nodeapi/TelegraphList?"
url2='https://www.cls.cn/v1/roll/get_roll_list?'
url3="https://www.cls.cn/nodeapi/updateTelegraphList?"






headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept':'application/json, text/plain, */*'}
news_num=100000
news_list = []
while len(news_list)<news_num:
    params1 = 'app=CailianpressWeb&category=&lastTime=' + str(last_time) + '&last_time=' + str(
        last_time) + '&os=web&refresh_type=1&rn=' + str(receive_num) + '&sv=7.5.5'
    params2 = 'app=CailianpressWeb&category=&lastTime=' + str(last_time) + '&last_time=' + str(
        last_time) + '&os=web&refresh_type=1&rn=' + str(receive_num) + '&sv=7.5.5'
    params3 = 'app=CailianpressWeb&category=&hasFirstVipArticle=0&lastTime=' + str(last_time) + '&os=web&rn=' + str(
        receive_num) + '&subscribedColumnIds=&sv=7.5.5'


    APIurl1 = url1 + params1 + '&sign=' + get_sign(params1)
    APIurl2 = url2 + params2 + '&sign=' + get_sign(params2)
    APIurl3 = url3 + params3 + '&sign' + get_sign(params3)

    resp = requests.get(APIurl1,headers=headers,verify = True)
    content = resp.json()['data']
    if content["roll_data"]==[]:
        resp = requests.get(APIurl2, headers=headers, verify=True)
        print("切换url")
        print(resp.json())
        content = resp.json()['data']
    print(content["roll_data"])
    last_time=content["roll_data"][-1]["ctime"]
    news_list.extend(getNewsDetail(content['roll_data']))

    time.sleep(0.5)

df = pd.DataFrame(news_list)
df.to_csv('财联社.csv')

