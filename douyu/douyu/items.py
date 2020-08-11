# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):

    nn = scrapy.Field()  #主播名称
    img_url = scrapy.Field() #直播间封面
