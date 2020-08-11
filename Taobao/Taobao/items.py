# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    img_url = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    svolume = scrapy.Field()
    evaluate = scrapy.Field()
    integral = scrapy.Field()
    detail_url = scrapy.Field()
