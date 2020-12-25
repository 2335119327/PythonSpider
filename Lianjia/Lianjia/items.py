# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    #城市
    city = scrapy.Field()
    #总价
    money = scrapy.Field()
    #地址
    address = scrapy.Field()
    # 房屋格局
    house_pattern = scrapy.Field()
    # 面积大小
    house_size = scrapy.Field()
    # 装修程度
    house_degree = scrapy.Field()
    # 楼层
    house_floor = scrapy.Field()
    # 单价
    price = scrapy.Field()