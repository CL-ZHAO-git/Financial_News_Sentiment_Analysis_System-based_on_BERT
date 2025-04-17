import threading
import time
res_data=[]
def thread_Timer1():

    global res_data
    # 声明全局变量
    #start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print("a")
    global t1
    # 创建并初始化线程
    t1 = threading.Timer(10, thread_Timer1)
    # 启动线程
    t1.start()


def thread_Timer2():
    global res_data
    # 声明全局变量
    # start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print("b")
    global t2
    # 创建并初始化线程
    t2 = threading.Timer(2, thread_Timer2)
    # 启动线程
    t2.start()

t1 = threading.Timer(10, thread_Timer1)
t1.start()
t2 = threading.Timer(2, thread_Timer2)
t2.start()