# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from BiliBili import settings
import os

class BilibiliPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        uname = item["uname"]
        img_cover = item["user_cover"]
        yield scrapy.Request(img_cover,meta={"uname":uname})

        img_crux = item['system_cover']
        yield scrapy.Request(img_crux,meta={"uname":uname})

    def file_path(self, request, response=None, info=None):
        file_name = request.url.split('/')[-1]
        file_name = file_name.split("?")[0]
        category = request.meta['uname']
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store,category)
        # print(category_path)
        # print("="*20)
        if not os.path.exists(category_path):
            image_name = os.path.join(category, file_name)
            name = image_name.split("\\")[1].split(".")[0]
            image_name = image_name.replace(name,"封面图")
            return image_name
        else:
            image_name02 = os.path.join(category, file_name)
            name1 = image_name02.split("\\")[1].split(".")[0]
            image_name02 = image_name02.replace(name1, "关键帧")
            return image_name02