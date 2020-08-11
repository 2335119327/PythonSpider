# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuyaItem(scrapy.Item):
    img_url = scrapy.Field()
    title = scrapy.Field()