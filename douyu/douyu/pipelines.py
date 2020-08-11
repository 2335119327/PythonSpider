# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from douyu import settings
import os

class DouyuPipeline(ImagesPipeline):

    #get_media_requests，该函数的作用是下载图片
    def get_media_requests(self, item, info):
        image_link = item["img_url"]
        image_name = item['nn']
        yield scrapy.Request(image_link,meta={"image_name":image_name})


    def file_path(self, request, response=None, info=None):
        # file_name = request.url.split('/')[-1]
        category = request.meta['image_name']
        # images_store = settings.IMAGES_STORE
        # category_path = os.path.join(images_store, category)
        # image_name = os.path.join(category, file_name)
        return category + ".jpg"
