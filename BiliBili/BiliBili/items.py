# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    uname = scrapy.Field()   #主播名称
    user_cover = scrapy.Field()  #封面图
    system_cover = scrapy.Field()  #关键帧