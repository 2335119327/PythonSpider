# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class TaobaoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TaobaoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


import random
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from PIL import Image
from scrapy.http.response.html import HtmlResponse


class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    ]

    def __init__(self):
        self.bro = webdriver.Chrome()

        # bro = webdriver.Chrome()
        self.bro.maximize_window()
        time.sleep(1)

        self.bro.get("https://login.taobao.com/member/login.jhtml")
        time.sleep(1)

        self.bro.find_element_by_class_name("icon-qrcode").click()
        time.sleep(3)

        # self.bro.find_element_by_name("fm-login-id").send_keys("18202781364")
        # time.sleep(1)
        # self.bro.find_element_by_name("fm-login-password").send_keys("wad07244058664")
        # time.sleep(1)
        #
        # # save_screenshot 就是将当前页面进行截图且保存
        # self.bro.save_screenshot('taobao.png')
        #
        # code_img_ele = self.bro.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
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
        # action = ActionChains(self.bro)
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
        # self.bro.find_element_by_xpath("//*[@id='login-form']/div[4]/button").click()

    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent



        # test_url = "https://s.taobao.com/search?q=java&s=0"
        self.bro.get(request.url)
        source = self.bro.page_source
        return HtmlResponse(url=request.url,body=source,request=request,encoding='utf-8')


