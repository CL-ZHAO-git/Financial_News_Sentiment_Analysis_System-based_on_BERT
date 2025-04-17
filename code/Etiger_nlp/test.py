import requests
import time
import pandas as pd
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
def getNewsDetail(item_list,no):
    news_list = []
    for item in item_list:
        news=OrderedDict()
        news['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item['display_time']))
        news['id'] = item['id']
        news['content'] = item['content_text']
        news["no"]=no
        news_list.append(news)
    return news_list

APIurl = 'https://api-prod.wallstreetcn.com/apiv1/content/lives'
url='http://api.wallstreetcn.com/v2/livenews'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept':'application/json, text/plain, */*'}

pc_params = {'channel':'a-stock-channel',
'client':'pc',
'cursor':1876211,
'limit':100,
}

news_list = []
for Loop_count in range(1):
    resp = requests.get(APIurl,headers=headers,params=pc_params,verify = True)
    content = resp.json()['data']
    pc_params['cursor'] = content['next_cursor']
    print(content['polling_cursor'])
    print(content['next_cursor'])
    print(content)

    news_list.extend(getNewsDetail(content['items'],pc_params['cursor']))
    print(news_list)

df = pd.DataFrame(news_list)
df.to_csv('华尔街.csv')

