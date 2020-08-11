# -*- coding: utf-8 -*-
import scrapy
import json
from douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'spider'
    # allowed_domains = ['www.douyu.com']
    start_urls = ['https://www.douyu.com/gapi/rknc/directory/yzRec/1']
    offset = 1


    def parse(self, response):

        data_list = json.loads(response.body)["data"]["rl"]
        for data in data_list:
            nn = data["nn"]
            img_url = data["rs1"]
            item = DouyuItem(nn=nn,img_url=img_url)
            yield item

        self.offset += 1
        if self.offset < 4:
            num = int(str(response).split(" ")[1].replace(">", "").split("/")[-1])
            num += 1
            url = "https://www.douyu.com/gapi/rknc/directory/yzRec/" + str(num)
            print(url)
            yield scrapy.Request(url=url,callback=self.parse,encoding="utf-8",dont_filter=True)