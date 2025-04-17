# coding=utf-8
import os
import re
import time

import requests
import urllib
def url_to_str(url):

    proxies={"http": None, "https": None}
    res=requests.get(url, proxies=proxies).text

    match = re.findall('<div class="rich_media_content " id="js_content" style="visibility: hidden;">(.*?)</div>',res,re.S|re.M)
    comp = re.compile('</?\w+[^>]*>')

    a=comp.sub('', match[0])
    a=a.replace(' ','')
    a=a.replace('\n','')
    a=a.replace('&gt;','\n')
    a=a.replace('&nbsp;','\n')
    a=a.replace('○','\n')
    a=a.replace('【','\n【')
    return a
