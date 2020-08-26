# -*- coding: utf-8 -*-
import scrapy
import time
from Lianjia.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://www.lianjia.com/city/']

    def parse(self, response):
        ul = response.xpath("//ul[@class='city_list_ul']/li")
        for li in ul:
            data_ul = li.xpath(".//ul/li")

            for li_data in data_ul:
                city = li_data.xpath(".//a/text()").get()
                page_url = li_data.xpath(".//a/@href").get() + "/ershoufang/"
                for i in range(3):
                    url = page_url + "pg" + str(i+1)
                    print(url)
                    yield scrapy.Request(url=url,callback=self.pageData,meta={"info":city})

    def pageData(self,response):
        print("="*50)
        city = response.meta.get("info")
        detail_li = response.xpath("//ul[@class='sellListContent']/li")
        for page_li in detail_li:
            if page_li.xpath("@class").get() == "list_app_daoliu":
                continue
            money = page_li.xpath(".//div[@class='totalPrice']/span/text()").get()
            money = str(money) + "万"
            address = page_li.xpath(".//div[@class='positionInfo']/a/text()").get()

            #获取到房屋的全部数据，进行分割
            house_data = page_li.xpath(".//div[@class='houseInfo']/text()").get().split("|")

            #房屋格局
            house_pattern = house_data[0]
            #面积大小
            house_size = house_data[1].strip()
            #装修程度
            house_degree = house_data[3].strip()
            #楼层
            house_floor = house_data[4].strip()
            #单价
            price = page_li.xpath(".//div[@class='unitPrice']/span/text()").get().replace("单价","")
            time.sleep(0.5)
            item = LianjiaItem(city=city,money=money,address=address,house_pattern=house_pattern,house_size=house_size,house_degree=house_degree,house_floor=house_floor,price=price)
            yield item


