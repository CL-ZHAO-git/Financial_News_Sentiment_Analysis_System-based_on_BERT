import pandas as pd
import numpy as np
from collections import OrderedDict
import json
from pymongo import MongoClient

import pandas as pd
myclient = MongoClient("mongodb://localhost:27017/")

db=myclient["News_Sentiment"]

mycol=db['bankuai']
def change(str):
    kt=str[:2]
    code=str[2:]
    new=code+'.'+kt
    return new

print(change("SH600426"))
df = pd.read_excel("板块.xlsx")
a=np.array(df['gn_name'])
gn_list=np.unique(a)
b={'name_list':gn_list}
#去掉列表中每一个元素的换行符


for bk in gn_list:
    code_list=list(df[df['gn_name']==bk]['instrumentid'])
    for i in range(len(code_list)):
        code_list[i]=change(code_list[i])
    mycol.insert_one({'name':bk,'code_list':code_list})

