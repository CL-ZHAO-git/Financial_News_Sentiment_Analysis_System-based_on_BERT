#--*- coding:utf-8 -*-------------------------------------------------------------------------------
# Name:        wallstreetcn
# Purpose:
#
# Author:      Administrator
#
# Created:     31/05/2016
# Copyright:   (c) Administrator 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import datetime
import requests
import lxml.html as lh
import csv
import json
#import urllib
import urllib.request
import pymongo
from pymongo import MongoClient
import sys

headers = {"Accept":"*/*",
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
headers1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept':'application/json, text/plain, */*'}

pageNo      = 1
keepWorking = 1
csvfile = open('wallstreetcn_history.csv', 'ab+')
writer = csv.writer(csvfile,delimiter=',',dialect='excel')
while(keepWorking):
    print (pageNo)

    url = "https://api-prod.wallstreetcn.com/apiv1/content/lives?limit=100&callback="+\
    "jQuery213007130278246278987_1464664591363&page="+str(pageNo) +"&_=1464664591377"
    url1="https://api-prod.wallstreetcn.com/apiv1/content/lives"
    params={"limit":100,'channel':'global-channel','cursor':pageNo}
    datas = urllib.parse.urlencode(params)
    new_url=url1+"?"+datas
    print(new_url)
    req = urllib.request.Request(new_url,headers=headers1)

    request     = urllib.request.urlopen(req).read()


    newRequest  = request[request.find(("data").encode())+9:len(request)-2]
    print(request)
    if  pageNo>5:                 #len(newRequest)<10:
        keepWorking = 0
        break
    else:
        jsonData    = json.loads(newRequest)
        for ii in range(0,len(jsonData)-1):
            if jsonData[ii]["id"] is not None:
                newsID           = jsonData[ii]["id"].encode('utf-8')
            if jsonData[ii]["title"] is not None:
                newsTitle        = jsonData[ii]["title"].decode('utf-8').encode('utf-8')
            if jsonData[ii]["createdAt"] is not None:
                newsCreated      = datetime.datetime.fromtimestamp(float(jsonData[ii]["createdAt"].encode('utf-8'))).strftime('%Y-%m-%d %H:%M:%S')
            if jsonData[ii]["updatedAt"] is not None:
                newsUpdated      = datetime.datetime.fromtimestamp(float(jsonData[ii]["updatedAt"].encode('utf-8'))).strftime('%Y-%m-%d %H:%M:%S')
            if jsonData[ii]["importance"] is not None:
                newsImportance   = jsonData[ii]["importance"].encode('utf-8')
            if jsonData[ii]["sourceName"] is not None:
                newsSource       = jsonData[ii]["sourceName"].encode('utf-8')
            if jsonData[ii]["node_color"] is not None:
                newsNodeColor    = jsonData[ii]["node_color"].decode('utf-8').encode('utf-8')
            if jsonData[ii]["node_format"] is not None:
                newsNodeFormat   = jsonData[ii]["node_format"].decode('utf-8').encode('utf-8')
            writer.writerow([newsID,newsTitle,newsCreated,newsUpdated,newsImportance,newsSource,newsNodeColor,newsNodeFormat])
            pageNo = pageNo +1
    # time.sleep(10)

csvfile.close()
#print jsonData[ii]["title"].decode('utf-8')
# print jsonData[ii]["node_color"]

#ii=0
