import requests
import time
import pandas as pd
from cls_crawler import getNewsDetail,get_time_stamp
from collections import OrderedDict
headers1 = {"Accept":"*/*",
           #"Accept-Encoding":"gzip, deflate, sdch",
           "Accept-Encoding":"none",
           "Accept-Language":"zh-CN,zh;q=0.8",
           "Connection":"keep-alive",
           "Cookie":"pgv_pvi=4959919104; wscnuid=CgQex1ZnnrAK/gf4A/CUAg==;"\
            "WSCN_SESSID=nufell5i3k7itj6b8l7k62kjh1;"\
            " __utma=81883081.201606728.1432881519.1464569114.1464654888.26;"\
            " __utmc=81883081; __utmz=81883081.1464569114.25.24."\
            "utmcsr=wallstreetcn.com|utmccn=(referral)|utmcmd=referral|utmcct=/node/246056;"\
            " Hm_lvt_c9477ef9d8ebaa27c94f86cc3f505fa5=1462236238,1463445192,1463530992;"\
            " Hm_lpvt_c9477ef9d8ebaa27c94f86cc3f505fa5=1464664598; "\
            "_ga=GA1.2.201606728.1432881519; _gat_newTracker=1",
            "DNT":"1",
            "Host":"api-prod.wallstreetcn.com",
            "Referer":"http://live.wallstreetcn.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36"\
            " (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"}


APIurl = 'https://api-prod.wallstreetcn.com/apiv1/content/lives'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept':'application/json, text/plain, */*'}


start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())#'2021-02-01 09:00:59'
end_time = '2021-02-04 14:35:59'
def get_wall_data(start_time):
    latest_time = get_time_stamp(start_time)
    end_time = latest_time-180
    pc_params = {'channel': 'a-stock-channel',
                 'client': 'pc',
                 'cursor': 0,
                 'limit': 1}
    news_list = []
    try:
        while latest_time >= end_time:
            resp = requests.get(APIurl,headers=headers1,params=pc_params,verify =True)
            content = resp.json()['data']
            pc_params['cursor'] = content['next_cursor']
                 #print(content['items'][0])

            latest_time = content['items'][-1]["display_time"]
            news_list.extend(getNewsDetail(content['items'],2,end_time))
        return news_list,False # 判断url是否过期 False 为url正常使用
    except:
        return [],True #表示url过期 需更新

# print(news_list)

#get_wall_data(start_time,end_time)