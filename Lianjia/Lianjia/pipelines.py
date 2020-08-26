# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class LianjiaPipeline:
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'lianjia',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None


    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['city'],item['money'],item['address'],item['house_pattern'],item['house_size'],item['house_degree']
                                      ,item['house_floor'],item['price']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                    insert into lianjia(id,city,money,address,house_pattern,house_size,house_degree,house_floor,price)
                    values(null,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql