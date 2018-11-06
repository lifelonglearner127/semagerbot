# -*- coding: utf-8 -*-
import scrapy


class KeywordsSpider(scrapy.Spider):
    name = 'keywords'
    allowed_domains = ['semager.de']
    start_urls = ['http://semager.de/']

    def parse(self, response):
        pass
