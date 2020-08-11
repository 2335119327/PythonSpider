# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import pymysql

class JingdongDownloadPipeline(ImagesPipeline):
    num = 0

    def get_media_requests(self, item, info):
        img_url = item['img_url']
        img_name = item['title']
        yield scrapy.Request(url=img_url,meta={"name":img_name},dont_filter=True)

    def file_path(self, request, response=None, info=None):
        name = request.meta["name"]
        self.num += 1
        img_name = str(name).replace("\t","").replace("\n","")
        return img_name + str(self.num) + ".jpg"

class JingdongPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'wad07244058664',
            'database': 'Jingdong',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self,item,spider):
        self.cursor.execute(self.sql, (item['img_url'], item['title'], item['price']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                        insert into jingdong(id,img_url,title,price)
                        values(null ,%s,%s,%s)
                    """
            return self._sql
        return self._sql
