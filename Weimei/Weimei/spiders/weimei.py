# -*- coding: utf-8 -*-
import scrapy
from Weimei.items import WeimeiItem
from bs4 import BeautifulSoup

class WeimeiSpider(scrapy.Spider):
    name = 'weimei'
    # allowed_domains = ['vmgirls.com']
    # start_urls = ['https://www.vmgirls.com/photography']

    data = {
        "append": "list - archive",
        "paged": "1",
        "action": "ajax_load_posts",
        "query": "17",
        "page": "cat"
    }

    def start_requests(self):
        for i in range(3):
            self.data["paged"] = str(1 + i)
            print(self.data["paged"])
            yield scrapy.FormRequest(url="https://www.vmgirls.com/wp-admin/admin-ajax.php", method='POST',
                                 formdata=self.data, callback=self.parse)

    def parse(self, response):
        bs1 = BeautifulSoup(response.text, "lxml")
        div_list = bs1.find_all(class_="col-md-4 d-flex")
        for div in div_list:
            a = BeautifulSoup(str(div), "lxml")
            page_url = a.find("a")["href"]
            name = a.find("a")["title"]
            yield scrapy.Request(url=page_url,callback=self.page,meta = {"name": name})

    def page(self,response):
        name = response.meta.get("name")
        bs2 = BeautifulSoup(response.text, "lxml")
        img_list = bs2.find(class_="nc-light-gallery").find_all("img")
        for img in img_list:
            image = BeautifulSoup(str(img), "lxml")
            img_url = "https://www.vmgirls.com/" + image.find("img")["data-src"]
            item = WeimeiItem(img_url=img_url, name=name)
            yield item
