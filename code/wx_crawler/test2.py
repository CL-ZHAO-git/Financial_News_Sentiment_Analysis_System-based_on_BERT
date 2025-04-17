# -*- coding: utf-8 -*-
import requests
import time
import json


# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

# 使用Cookie，跳过登陆操作
headers = {
  "Cookie": 'ua_id=77wODa00P4tjCPc1AAAAALY54P5i1nxGUphs3c2Harg=; uuid=dfa602566a1e0e1a9fe6ee215f06214b; bizuin=3922218236; ticket=5f8c46ef2b23a9efdaeac122a6f142320b581a53; ticket_id=gh_6a582b3a26c4; cert=M1_MOxESqwavuhEgpT7hd2NVvfLzLGQG; noticeLoginFlag=1; rand_info=CAESIH8Y45LxIHJLgOnjPnzViitbXjy5cLL/aMRNKx+G1IrG; slave_bizuin=3922218236; data_bizuin=3922218236; data_ticket=SouoLo2A3w2Jx4AtB5ykbWUHTR6GFmMafa7WtxdrXSj4ELPyY0hRf34W/X+kve0m; slave_sid=cW9XX212blJFSGkzcjdiUnVqRGhvaldpM1dBR0N6a2dmdXRNVDhNSm40Y3J4NUE3TFlwSENXbnluMWxkSUJvTG9pd185WkpNUUVqQlhiZVhxR1BsSzJDMmRVUnNTTTJVUFVzVXZPQWxkaGkwNkx3TnJ0RkZGTnV5ajVrTlRLOXZlMFJkWVlvQVZxNFdVcmlO; slave_user=gh_6a582b3a26c4; xid=11251c9569b701d6d75fb6f97f3241a1; openid2ticket_o_EzI6VzZVjcaXBapIFmbcvlazHQ=g7Fe7gi/P5GqYTlBps2F2PB9LFcheYxCBqIRax/GMX0=; mm_lang=zh_CN',
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
}

"""
需要提交的data
以下个别字段是否一定需要还未验证。
注意修改yourtoken,number
number表示从第number页开始爬取，为5的倍数，从0开始。如0、5、10……
token可以使用Chrome自带的工具进行获取
fakeid是公众号独一无二的一个id，等同于后面的__biz
"""
data = {
    "token": 574576476,
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": 0,
    "count": "5",
    "query": "",
    "fakeid": 'MzIxNDUxNTAxMQ==',
    "type": "9",
}

# 使用get方法进行提交
content_json = requests.get(url, headers=headers, params=data).json()
# 返回了一个json，里面是每一页的数据
for item in content_json["app_msg_list"]:
    # 提取每页文章的标题及对应的url
    print(item["title"], "url",item["link"])