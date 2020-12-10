# -*- coding: utf-8 -*-
# ##############################
# ###### writen by song ########
# ##############################
"""
reference link : https://github.com/MakiNaruto/Automatic_ticket_purchase
get more details in readme.md
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

# 大麦网主页
damai_url = "https://www.damai.cn/"
# 登录页
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
# 抢票目标页
target_url = \
"https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.36171aa0WuyGBf&id=630543617994&clicktitle=%E5%BE%B7%E4%BA%91%E7%A4%BE%E7%9B%B8%E5%A3%B0%E5%A4%A7%E4%BC%9A%EF%BC%88%E5%8D%97%E4%BA%AC%E8%80%81%E9%97%A8%E4%B8%9C%EF%BC%89-%E5%8D%97%E4%BA%AC%E5%BE%B7%E4%BA%91%E7%A4%BE%E5%89%A7%E5%9C%BA"


class Concert(object):
    def __init__(self):
        self.status = 0  # 状态,表示如今进行到何种程度
        self.login_method = 1  # {0:模拟登录,1:Cookie登录}自行选择登录方式

    def set_cookie(self):
        self.driver.get(damai_url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            sleep(1)
        print('###请扫码登录###')

        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
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
        if self.login_method == 0:
            self.driver.get(login_url)  # 载入登录界面
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):  # 如果不存在cookie.pkl,就获取一下
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()

    def enter_concert(self):
        print("=" * 30)
        print('###打开浏览器，进入大麦网###')
        self.driver = webdriver.Chrome(
            executable_path='chromedriver')
        self.driver.maximize_window() # max window
        self.login()
        self.driver.refresh()
        self.status = 2
        print("###登录成功###")


    def choose_ticket(self):
        if self.status == 2:  # 登录成功0入口
            self.num = 1  # 第一次尝试
            print("=" * 30)
            print("###开始进行日期及票价选择###")
            while self.driver.title.find('确认订单') == -1:  # 如果跳转到了订单结算界面就算这步成功了，否则继续执行此步
                print('### Confirm ###')
                try:
                    print("### 身份确认 ###")
                    self.driver.find_element_by_xpath("//div[@class='realname-popup-wrap']/div[@class='operate']/div[@class='button']")
                    self.driver.find_element_by_xpath("//div[@class='realname-popup-wrap']/div[@class='operate']/div[@class='button']").click()
                except:
                    print("### 没有身份确认 ###")
                cart = self.driver.find_element_by_class_name('perform')  # 获得选票界面的表单值
                # try:各种按钮的点击,
                buybutton = self.driver.find_element_by_class_name('buybtn').text
                try:
                    buybutton = self.driver.find_element_by_class_name('buybtn').text
                    if buybutton == "提交缺货登记" or buybutton == "即将开抢":
                        self.status = 2
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
                print('now page title is', title)
                if title == '选座购买':
                    self.choice_seats()
                # 确认订单
                if self.isElementExist('//*[@id="confirmOrder_1"]/div[2]/div[1]'):
                    self.check_order()
                try:
                    element = WebDriverWait(self.driver, 2, 1).until(
                    EC.presence_of_element_located((By.ID, "container")))
                    print("### 抢票成功 请支付订单！###")
                    break
                except:
                    self.status = 2
                    self.driver.get(target_url)
                    print('###抢票失败，从新开始抢票###')

    def choice_seats(self):
        while self.driver.title == '选座购买':
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/img'):
                print('请快速的选择您的座位！！！')
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[2]/div'):
                self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/button').click()

    def check_order(self):
        if self.status in [3, 4, 5]:
            print('###开始确认订单###')
            try:
                # 默认选第一个购票人信息
                self.driver.find_element_by_xpath(
                    '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div[1]/label/span[1]').click()

            except Exception as e:
                print("###购票人信息选中失败，自行查看元素位置###")

            # 最后一步提交订单
            time.sleep(0.1)  # 太快会影响加载，导致按钮点击无效
            # self.driver.find_element_by_link_text(u'同意以上协议并提交订单').click()

            self.driver.find_elements_by_xpath("//button[@class='next-btn next-btn-normal next-btn-medium']")[-1].click()
            # self.driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div/div[9]/button')[0].click()


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
        # start!
        con = Concert()
        con.enter_concert()  # log in
        con.choose_ticket()

    except Exception as e:
        print('ERROR FOR :::', e)
        # con.finish()
