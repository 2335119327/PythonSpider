# -*- coding: utf-8 -*-
import scrapy
from Jingdong.items import JingdongItem
import time


class JdSpider(scrapy.Spider):
    name = 'JD'
    allowed_domains = ['jingdong.com']
    start_urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&page=1&s=1&click=0']
    num = 1
    s = 1
    def parse(self, response):
        time.sleep(0.5)
        ul_list = response.xpath("//ul[@class='gl-warp clearfix']/li")
        for ul in ul_list:
            img_url = "http:" + ul.xpath(".//img/@src").get()
            price = ul.xpath(".//i/text()").get()
            title = ul.xpath(".//div[@class='p-name p-name-type-2']//em/text()").get()
            item = JingdongItem(img_url=img_url,title=title,price=price)
            yield item
        self.s += 50
        self.num += 2
        next_url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&page=" + str(self.num) + "&s=" + str(self.s) + "&click=0"
        if self.num <= 7:
            print(next_url)
            print(self.num)
            yield scrapy.Request(url=next_url,callback=self.parse,encoding="utf-8",dont_filter=True)
