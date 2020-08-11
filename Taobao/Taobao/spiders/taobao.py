# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from Taobao.items import TaobaoItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://s.taobao.com/search?q=java&s=0']


    #登录
    def login(self,url):
        bro = webdriver.Chrome()
        bro.maximize_window()
        time.sleep(1)

        bro.get(url)
        time.sleep(1)

        bro.find_element_by_class_name("icon-qrcode").click()
        time.sleep(3)

        # bro.find_element_by_name("fm-login-id").send_keys("18202781364")
        # time.sleep(1)
        # bro.find_element_by_name("fm-login-password").send_keys("wad07244058664")
        # time.sleep(1)
        #
        # # save_screenshot 就是将当前页面进行截图且保存
        # bro.save_screenshot('taobao.png')
        #
        # code_img_ele = bro.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
        # location = code_img_ele.location  # 验证码图片左上角的坐标 x,y
        # size = code_img_ele.size  # 验证码的标签对应的长和宽
        # # 左上角和右下角的坐标
        # rangle = (
        #     int(location['x']), int(location['y']), int(location['x'] + size['width']),
        #     int(location['y'] + size['height'])
        # )
        #
        # i = Image.open("./taobao.png")
        # # crop裁剪
        # frame = i.crop(rangle)
        #
        # # 动作链
        # action = ActionChains(bro)
        # # 长按且点击
        # action.click_and_hold(code_img_ele)
        #
        # # move_by_offset(x,y) x水平方向,y竖直方向
        # # perform()让动作链立即执行
        # action.move_by_offset(260, 0).perform()
        # time.sleep(0.5)
        #
        # # 释放动作链
        # action.release()
        # # 登录
        # bro.find_element_by_xpath("//*[@id='login-form']/div[4]/button").click()
        return bro



    def parse(self, response):
        response = str(response).split(" ")[1].replace(">","")
        bro = self.login(response)
        # print(response.text)
        num = 0
        for i in range(2):
            url = "https://s.taobao.com/search?q=java&s=" + str(num)
            num += 44
            bro.get(url)
            html = bro.page_source

            soup = BeautifulSoup(html, 'lxml')
            data_list = soup.find_all(class_='item J_MouserOnverReq')
            for data in data_list:
                data_soup = BeautifulSoup(str(data), 'lxml')
                # 图片链接
                img_url = "http:" + data_soup.find(class_='J_ItemPic img')['data-src']
                # 图片价格
                price = data_soup.find('strong').string
                # 图片标题
                title = data_soup.find(class_='J_ItemPic img')['alt']
                # 详情页
                detail_url = "https:" + data_soup.find(class_="pic-link J_ClickStat J_ItemPicA")["data-href"]

                bro.get(detail_url)
                time.sleep(1)
                html_second = bro.page_source
                soup = BeautifulSoup(html_second, 'lxml')

                try:
                    svolume = soup.find(class_="tm-ind-item tm-ind-sellCount").text.replace("月销量", "")
                except:
                    svolume = 0

                try:
                    evaluate = soup.find(class_="tm-ind-item tm-ind-reviewCount canClick tm-line3").text.replace("累计评价", "")
                except:
                    evaluate = 0

                try:
                    integral = soup.find(class_="tm-ind-item tm-ind-emPointCount").text.replace("送天猫积分", "")
                except:
                    integral = 0

                item = TaobaoItem(img_url=img_url, price=price, title=title, svolume=svolume, evaluate=evaluate,
                                  integral=integral, detail_url=detail_url)
                yield item
