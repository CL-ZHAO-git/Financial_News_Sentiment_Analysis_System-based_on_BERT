

import time
import datetime
def get_time_stamp(date):
    timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

start_time='2021-01-29 09:00:59'
end_time='2017-01-29 09:00:59'
start_time=get_time_stamp(start_time)
end_time=get_time_stamp(end_time)
a=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(1612419920))
b=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(1612419620))
print(start_time)
print(a)
print(b)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))