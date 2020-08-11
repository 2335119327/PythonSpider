# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os


class WeimeiPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_url = item["img_url"]
        name = item["name"]
        # print(img_url)
        yield scrapy.Request(url=img_url, meta={"name": name})

    def file_path(self, request, response=None, info=None):
        name = request.meta["name"]
        img_name = request.url.split('/')[-1]
        img_path = os.path.join(name,img_name)
        # print(img_path)
        return img_path  # 返回文件名


    def item_completed(self, results, item, info):
        # print(item)
        return item  # 返回给下一个即将被执行的管道类
