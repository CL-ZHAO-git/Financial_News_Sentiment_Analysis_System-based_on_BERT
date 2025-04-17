#!usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib.request
import datetime


#链接数据库test

#网站默认的最原始时间
starttime=datetime.datetime(1970,1,1,8,0,0)

#读取新闻内容接口
response = urllib.request.urlopen('https://api.wallstreetcn.com/v2/livenews?limit=1000')#可以继续研究两个时间段内的新闻接口代码
http=response.read()
hjson = json.loads(http.decode())
print(hjson)

#获取想要的新闻内容和时间
for i in range (0,len(hjson['results'])):#len(hjson['results'])为results整个条目数
    time=hjson['results'][i]['createdAt']
    content=hjson['results'][i]['contentText']
 #print(starttime+ datetime.timedelta(seconds=int(time)))
 #print(content)

 #识别时间
    time1=starttime+ datetime.timedelta(seconds=int(time))#识别
    tim1=datetime.datetime.strftime(time1,'%Y-%m-%d %H:%M:%S')#将时间换算成字符串
 #print(datetime.datetime.strftime(time1,'%Y-%m-%d %H:%M:%S'))
    print(content)


#关闭数据库
