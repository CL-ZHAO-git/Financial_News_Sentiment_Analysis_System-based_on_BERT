import time,datetime
import pandas as pd
date='2021-01-21 09:00:59'
print(date[:-3])
date_ = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
#print(date_>datetime.datetime(""))
a=(date_.time().strftime('%H:%M')+datetime.timedelta(minutes=5)).strftime('%Y-%m-%d')
b="09:15"
print(a)
timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray))
print(timeStamp)
#print((a>="11:30")&(a<"13:00"))
def judge_date_status(date):
    '''
    :param date: 
    :return: 0 交易时段
             1 交易日 收盘时间 0-9点
             2 交易日（除周五） 收盘时间 15-24点
             3 交易日 午间休市
             4 周五 收盘时间 15-24点
             5 周六
             6 周日
    '''
    date_ = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    time= date_.time().strftime('%H:%M')
    if date_.weekday() in [0,1,2,3,4]:
        if time > "9:00" and time < "15:00":
            if (time>="11:30")&(time<"13:00"):
                return 3
            else :
                return 0
        elif time <= "9:00":
            return 1
        elif time >= "15:00":
            if date_.weekday()==4:
                return 4
            else:
                return 2
    else:
        return date_.weekday()

            #if


print(judge_date_status(date))
print(int(time.time()))