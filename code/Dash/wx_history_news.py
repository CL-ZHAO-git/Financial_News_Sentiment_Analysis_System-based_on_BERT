from selenium import webdriver
import re
import time
import random
from functools import reduce
from pprint import pprint
import pandas as pd
import pinyin
import urllib.request
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from url_to_html import  url_to_str
"""
note: 需要使用selenium，chrome版本需要与chromedriver版本对应。具体见https://chromedriver.storage.googleapis.com/
该文件仅作测试用，可能失效
"""
from pymongo import MongoClient
myclient = MongoClient("mongodb://localhost:27017/")
db_wx=myclient['wx_public']

class have_multi_pages():
    def __call__(self, driver):
        if len(driver.window_handles) > 1:
            return True
        else:
            return False

def login(username, password,driver,img_name):
    # 打开微信公众号登录页面
    driver.get("https://mp.weixin.qq.com/")
    driver.maximize_window()
    time.sleep(0.5)
    # 自动填充帐号密码

    # 点击使用账号密码登陆
    driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/a'
    ).click()
    # 输入账号
    driver.find_element_by_xpath(

        '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input'
    ).clear()
    driver.find_element_by_xpath(
        '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input'
    ).send_keys(username)
    # 输入密码
    driver.find_element_by_xpath(
        '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input'
    ).clear()
    driver.find_element_by_xpath(
        '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input'
    ).send_keys(password)

    WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH,'//*[@id="header"]/div[2]/div/div/div[1]/form/div[4]/a')))
    # 自动点击登录按钮进行登录
    driver.find_element_by_xpath(
        '//*[@id="header"]/div[2]/div/div/div[1]/form/div[4]/a'
        #'//*[@id="header"]/div[2]/div/div/form/div[4]/a'
    ).click()
    #//*[@id="app"]/div[3]/div/div[2]/div[1]/div/img
    # 拿手机扫二维码！
    WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div[1]/div/img')))
    driver.find_element_by_xpath(
        '//*[@id="app"]/div[3]/div/div[2]/div[1]/div/img'
        # '//*[@id="header"]/div[2]/div/div/form/div[4]/a'
    ).screenshot("QRcode_images/"+img_name)
    print('开始等待')
    WebDriverWait(driver,180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="menuBar"]/li[2]/ul/li[1]/a/span/span')))
    print('等待结束')#time.sleep(15)

def date2num(date):
    date = date.replace('-', '')

    date = int(date)
    return date

def open_link(driver):
    print("开始定位")
    #time.sleep(20)

    # 进入新建图文素材
    #time.sleep(2)
    WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="menuBar"]/li[2]/ul/li[1]/a/span/span')))
    print("找到了")
    driver.find_element_by_xpath(
        '//*[@id="menuBar"]/li[2]/ul/li[1]/a/span/span'
    ).click()
    print("click")
    new_button=driver.find_element_by_xpath('//*[@id="js_main"]/div[3]/div[2]/div/div/div/div[1]/div/div/div[1]')
    ActionChains(driver).move_to_element(new_button).perform()
    driver.find_element_by_xpath(
        '//*[@id="js_main"]/div[3]/div[2]/div/div/div/div[1]/div/div/div[2]/ul/li[1]/a'
    ).click()
    time.sleep(0.5)
    print("开始等待2")
    WebDriverWait(driver, 30).until(have_multi_pages())
    print("结束等待2")
    # 切换到新窗口
    for handle in driver.window_handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)

    # 点击超链接
    driver.find_element_by_xpath('//*[@id="js_editor_insertlink"]').click()
    WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/p/div/button')))
    # 点击选择其他公众号
def open_search(driver,nickname):
    pinyin_name = getStrAllAplha(nickname)  # 公众号名称
    driver.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/p/div/button').click()
    # 输入公众号名称
    driver.find_element_by_xpath(
        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/input'
    ).clear()
    driver.find_element_by_xpath(
        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/input'
    ).send_keys(nickname)
    # 点击搜索
    driver.find_element_by_xpath(
        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[1]/span/input'
    ).send_keys(Keys.ENTER)
    WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH,'//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[2]/ul/li[1]/div[1]')))
    # 点击第一个公众号
    driver.find_element_by_xpath(
        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[2]/ul/li[1]/div[1]'
    ).click()
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div[3]/span[1]/span/label[2]')))
    page_num = int(
        driver.find_element_by_xpath(
            '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div[3]/span[1]/span/label[2]').text)
    print(page_num)
    # 点击下一页
    url_title_lst, is_over = get_url_title(driver.page_source, driver, pinyin_name,nickname)
    print("第{}页成功".format(1))
    # print(url_title_lst)
    if is_over:
        #print(url_title_lst)
        print("第一次结束")
        # print(url_title_lst)
        driver.quit()
        df=pd.DataFrame(url_title_lst)
        df.to_csv('wx_jc_history.csv')
        return url_title_lst
    else:
        pagination = driver.find_elements_by_class_name("weui-desktop-pagination")[0]
        pagination.find_elements_by_tag_name("a")[0].click()
        for _ in range(1, page_num):
            try:

                time.sleep(30+random.randint(0,10))
                lst, is_over2 = get_url_title(driver.page_source, driver, pinyin_name,nickname)
                url_title_lst += lst
                if is_over2:
                    print("结束2")
                    driver.quit()
                    #print(url_title_lst)
                    df = pd.DataFrame(url_title_lst)
                    df.to_csv('wx_jc_history.csv')
                    return url_title_lst
                else:
                    print("第{}页成功".format(_+1))
                    pagination = driver.find_elements_by_class_name("weui-desktop-pagination")[0]
                    pagination.find_elements_by_tag_name("a")[1].click()
                    df = pd.DataFrame(url_title_lst)
                    print(df)
                    df.to_csv('wx_jc_history.csv')
                # print(url_title_lst)
            except:  # 保存
                print("第{}页失败".format(_))
                df = pd.DataFrame(url_title_lst)
                df.to_csv('wx_jc_history.csv')
                continue
    df = pd.DataFrame(url_title_lst)
    df.to_csv('wx_jc_history.csv')
    return url_title_lst
    #time.sleep(3)


def get_url_title(html,driver,name,nickname):
    global db_wx
    mycol=db_wx[name]
    lst = []
    is_over=False # 表示数据库中无该数据 需要添加。当爬取结果中有
    for item in driver.find_elements_by_class_name("inner_link_article_item"):# 爬取按时间顺序
        new = OrderedDict()

        new["date"]= item.find_element_by_class_name("inner_link_article_date").text
        new["title"]= item.find_element_by_class_name("inner_link_article_title").text
        new["url"]= item.find_element_by_tag_name("a").get_attribute('href')
        new['date_num']= date2num(item.find_element_by_class_name("inner_link_article_date").text)
        new['account'] = nickname
        try:
            new['content']=url_to_str(item.find_element_by_tag_name("a").get_attribute('href'))
        except:
            print("解析url失败")
            new['content']="解析url失败"

        if name=="cls":
            if new['title'].find('早报')!=-1:
                pass
            else:
                continue
        a = mycol.insert_one(new)
    return lst,is_over


# 用webdriver启动谷歌浏览器
def get_artical_data(nickname):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('window-size=1366x768')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(executable_path="/Users/zcl271828/PycharmProjects/WebCrawler/chromedriver",chrome_options=options)
    img=str(time.time())+'.png'

    username = "etiger_nlp@163.com"  # 账号
    password = "et123456"  # 密码
    login(username, password,driver,img)
    open_link(driver)
    url_title_lst=open_search(driver,nickname)
    print()
    time.sleep(1)
    print("结束3")

    #print(driver.find_elements_by_class_name("page_num"))
    #print(driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[6]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div[3]/span[1]/span/label[2]').text)

    driver.quit()
    print(url_title_lst)
    return url_title_lst

def getStrAllAplha(str):
    return pinyin.get_initial(str, delimiter="")

get_artical_data('财联社')
#print('早报222222'.find('3'))