# -*- coding:utf-8 -*------------------------------------------------------------------------
# Name:        抓取主要网站新闻内容
# Purpose:      网站信息 抓取频率1分钟
# http://news.cnstock.com/news/sns_yw    中国证券网-要闻
# 记录信息：信息标号，标题，时间，来源，suburl
#
# Author:      Administrator
#
# Created:     30/03/2016
# Copyright:   (c) Administrator 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib
import lxml.html as lh
import datetime
import pandas as pd
from sqlalchemy import create_engine

#pageNo = 117741

for pageNo in range(270150,271995):

    url = 'http://api.cailianpress.com/v1/share/article_detail?article_id='+str(pageNo)+'&from=singlemessage&isappinstalled=1'
    req = urllib.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36')
    try:
        request     = urllib.urlopen(req).read()
        tree        = lh.fromstring(request)

        body_content        = tree.xpath('.//div[@class="body_content"]')
        if len(body_content)>0:
            article_title = body_content[0].xpath('.//p[@class="article_title"]')
            article_info = body_content[0].xpath('.//p[@class="article_info"]')

            info_time = article_info[0].xpath('.//font[@class="info_time"]')
            info_author = article_info[0].xpath('.//font[@class="info_author"]')
            article_content = body_content[0].xpath('.//div[@class="article_content"]')

            try:
                title = article_title[0].text
                time = info_time[0].text
                author = info_author[0].text
                content = article_content[0].text_content()
            except:
                print(str(pageNo)+"error!")
            newsInfo = pd.DataFrame()
            newsInfo.loc[0,"LastUpdateTime"] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            newsInfo.loc[0,"DateTime"] = time
            newsInfo.loc[0,"PageNo"] = pageNo
            newsInfo.loc[0,"Title"] = title
            newsInfo.loc[0,"Author"] = author
            newsInfo.loc[0,"Content"] = content
            newsInfo.to_csv(pageNo+'.csv')

    print(str(pageNo)+"insert!")



