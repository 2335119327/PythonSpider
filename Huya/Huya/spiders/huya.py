# -*- coding: utf-8 -*-
import scrapy
import json
from Huya.items import HuyaItem

class HuyaSpider(scrapy.Spider):
    name = 'huya'
    allowed_domains = ['huya.com']
    start_urls = ['https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=1663&tagAll=0&page=1']
    num = 1

    def parse(self, response):
        data_list = json.loads(response.text,encoding='utf-8')
        datas = data_list["data"]["datas"]
        for data in datas:
            img_url = data["screenshot"]
            title = data["nick"]
            item = HuyaItem(img_url=img_url,title=title)
            yield item

        self.num += 1
        if self.num <= 3:
            next_url = "https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=1663&tagAll=0&page=" + str(self.num)
            yield scrapy.Request(url=next_url,encoding="utf-8")