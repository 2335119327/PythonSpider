# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        avatar = response.xpath("//div[@class='_2mYfmT']/a/img/@src").get()
        author = response.xpath("//span[@class='FxYr8x']/a[@class='_1OhGeD']/text()").get()
        put_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        url = response.url
        content = response.xpath("//article[@class='_2rhmJa']").get()
        article_id = url.split("/")[-1]

        word_count = response.xpath("//div[@class='s-dsoj']/span[2]").get()
        comment_count = response.xpath("//div[@class='_3nj4GN'][1]/span").get()
        like_count = response.xpath("//div[@class='_3nj4GN'][2]/span").get()
        read_count = response.xpath("//div[@class='s-dsoj']/span[3]").get()

        subjects = ",".join(response.xpath("//div[@class='_2Nttfz']/a/span/text()").getall())


        item = ArticleItem(title=title,
                           author=author,
                           avatar=avatar,
                           put_time=put_time,
                           article_id=article_id,
                           origin_url=url,
                           content=content,
                           word_count=word_count,
                           comment_count=comment_count,
                           like_count=like_count,
                           read_count=read_count,
                           subjects=subjects)
        yield item



