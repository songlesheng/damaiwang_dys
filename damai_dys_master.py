# -*- coding: utf-8 -*-
# ##############################
# ###### writen by song ########
# ##############################
"""
reference link : https://github.com/MakiNaruto/Automatic_ticket_purchase
get more details in readme.md
email : 18020090018@pop.zjgsu.edu.cn
"""
import os
import re
import time
import pickle
from tkinter import *
from time import sleep
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


#大麦网主页
damai_url="https://www.damai.cn/"
#登录页
login_url="https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
#抢票目标页
target_url ='https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.227928dfl6DiPP&id=610046670076&clicktitle=%E5%91%A8%E6%9D%B0%E4%BC%A6%E3%80%90%E5%98%89%E5%B9%B4%E5%8D%8E%E3%80%91%E4%B8%96%E7%95%8C%E5%B7%A1%E5%9B%9E%E6%BC%94%E5%94%B1%E4%BC%9A%E6%B7%B1%E5%9C%B3%E7%AB%99'
name = ""
phone = ""


class Concert(object):
    def __init__(self):
        self.status = 0         # 状态,表示如今进行到何种程度
        self.login_method = 1   # {0:模拟登录,1:Cookie登录}自行选择登录方式
    def set_cookie(self):
       self.driver.get(damai_url)
       print("###请点击登录###")
       while self.driver.title.find('大麦网-全球演出赛事官方购票平台') !=-1:
            sleep(1)
       print('###请扫码登录###')

       while self.driver.title!='大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
           sleep(1)
       print("###扫码成功###")
       pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
       print("###Cookie保存成功###")
       self.driver.get(target_url) 

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))#载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain':'.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)
            
    def login(self):
        if self.login_method==0:
            self.driver.get(login_url)                                #载入登录界面
            print('###开始登录###')

        elif self.login_method==1:            
            if not os.path.exists('cookies.pkl'):                     #如果不存在cookie.pkl,就获取一下
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()

    def enter_concert(self):
        print('###打开浏览器，进入大麦网###') 
        self.driver = webdriver.Chrome(executable_path='C:\\Users\Song Lesheng\Desktop/taobao\chromedriver')        #默认Chrome浏览器
        # self.driver.maximize_window()           #最大化窗口
        self.login()                            #先登录再说
        self.driver.refresh()                   #刷新页面
        self.status = 2                         #登录成功标识
        print("###登录成功###")

    def choose_ticket(self):
        if self.status == 2:                  #登录成功入口
            self.num = 1                      #第一次尝试

            print("="*30)
            print("###开始进行日期及票价选择###")
            while self.driver.title.find('确认订单') == -1:           # 如果跳转到了订单结算界面就算这步成功了，否则继续执行此步

                cart = self.driver.find_element_by_class_name('perform')   # 获得选票界面的表单值
                # try:各种按钮的点击,
                buybutton = self.driver.find_element_by_class_name('buybtn').text
                try:
                    buybutton = self.driver.find_element_by_class_name('buybtn').text
                    if buybutton == "提交缺货登记":
                        self.status=2
                        self.driver.get(target_url)
                        print('###抢票未开始，刷新等待开始###')
                        continue
                    elif buybutton == "立即预定":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 3
                        self.num = 1
                    elif buybutton == "立即购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 4

                    # 选座购买暂时无法完成自动化
                    elif buybutton == "选座购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        # self.driver.find_element_by_class_name('price').click()
                        self.status = 5

                except:
                    print('###未跳转到订单结算界面###')
                
                title = self.driver.title
                if title == '选座购买':
                    self.choice_seats()

                while True:
                    print('waiting ......')
                    if self.isElementExist('//*[@id="confirmOrder_1"]/div[1]/div[2]/div[1]/div[1]'):
                        self.check_order()
                        break

                # if title !="确认订单" : #如果前一次失败了，那就刷新界面重新开始
                #     self.status=2
                #     self.driver.get(target_url)
                #     print('###抢票失败，从新开始抢票###')

    def choice_seats(self):

        while self.driver.title == '选座购买':
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/img'):
                print('请快速的选择您的座位！！！')
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[2]/div'):
                self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/button').click()

    def check_order(self):
        if self.status in [3,4,5]:
            print('###开始确认订单###')

            try:
                # 默认选第一个购票人信息
                self.driver.find_element_by_xpath('//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div[1]/label/span[1]').click()

            except Exception as e:
                print("###购票人信息选中失败，自行查看元素位置###")
                print(e)

            # 最后一步提交订单

            time.sleep(0.5)  # 太快会影响加载，导致按钮点击无效
            self.driver.find_elements_by_xpath('//div[@class = "w1200"]//div[2]//div//div[9]//button[1]')[0].click()

    def finish(self):
        self.driver.quit()

    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag

        except:
            flag = False
            return flag


if __name__ == '__main__':
    try:
        con = Concert()             #具体如果填写请查看类中的初始化函数
        con.enter_concert()
        con.choose_ticket()

    except Exception as e:
        print(e)
        con.finish()
