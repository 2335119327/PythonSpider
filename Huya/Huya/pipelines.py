# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class HuyaPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_url = item["img_url"]
        title = item["title"]
        yield scrapy.Request(url=img_url,meta={"title":title})


    def file_path(self, request, response=None, info=None):
        name = request.meta["title"]
        return name + '.jpg'