# -*- coding: utf-8 -*-
import scrapy
import json
from BiliBili.items import BilibiliItem


class BzSpider(scrapy.Spider):
    name = 'bz'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=sort_type_152&page=1&page_size=30']
    num = 1

    def parse(self, response):
        print(response)
        data_list = json.loads(response.text)["data"]["list"]

        for data in data_list:
            uname = data['uname']
            user_cover = data["user_cover"]
            system_cover = data["system_cover"]

            item = BilibiliItem(uname=uname,user_cover=user_cover,system_cover=system_cover)
            yield item
        self.num += 1
        url = "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=sort_type_152&page=" + str(self.num) + "&page_size=30"

        if self.num <= 4:
            yield scrapy.Request(url=url,callback=self.parse)

