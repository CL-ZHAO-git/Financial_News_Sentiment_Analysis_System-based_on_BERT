import os
from pprint import pprint
from wechatarticles import PublicAccountsWeb
from wechatarticles.utils import save_json

if __name__ == "__main__":
    # 模拟登录微信公众号平台，获取微信文章的url
    cookie = "appmsglist_action_3922218236=card; ua_id=77wODa00P4tjCPc1AAAAALY54P5i1nxGUphs3c2Harg=; uuid=dfa602566a1e0e1a9fe6ee215f06214b; bizuin=3922218236; ticket=5f8c46ef2b23a9efdaeac122a6f142320b581a53; ticket_id=gh_6a582b3a26c4; cert=M1_MOxESqwavuhEgpT7hd2NVvfLzLGQG; noticeLoginFlag=1; rand_info=CAESIH8Y45LxIHJLgOnjPnzViitbXjy5cLL/aMRNKx+G1IrG; slave_bizuin=3922218236; data_bizuin=3922218236; data_ticket=SouoLo2A3w2Jx4AtB5ykbWUHTR6GFmMafa7WtxdrXSj4ELPyY0hRf34W/X+kve0m; slave_sid=cW9XX212blJFSGkzcjdiUnVqRGhvaldpM1dBR0N6a2dmdXRNVDhNSm40Y3J4NUE3TFlwSENXbnluMWxkSUJvTG9pd185WkpNUUVqQlhiZVhxR1BsSzJDMmRVUnNTTTJVUFVzVXZPQWxkaGkwNkx3TnJ0RkZGTnV5ajVrTlRLOXZlMFJkWVlvQVZxNFdVcmlO; slave_user=gh_6a582b3a26c4; xid=11251c9569b701d6d75fb6f97f3241a1; openid2ticket_o_EzI6VzZVjcaXBapIFmbcvlazHQ=g7Fe7gi/P5GqYTlBps2F2PB9LFcheYxCBqIRax/GMX0=; mm_lang=zh_CN"
    token = "574576476"
    nickname = "爱在冰川同学"
    #query = "query"

    paw = PublicAccountsWeb(cookie=cookie, token=token)
    articles_sum = paw.articles_nums(nickname)
    article_data = paw.get_urls(nickname)
    #official_info = paw.official_info(nickname)

    print("articles_sum:", end=" ")
    print(articles_sum)
    print("artcles_da:")
    pprint(article_data)
    # print("official_info:")
    # pprint(official_info)

    #save_json("paw.json", article_data)