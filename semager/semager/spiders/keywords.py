# -*- coding: utf-8 -*-
import scrapy


class KeywordsSpider(scrapy.Spider):
    name = 'keywords'
    allowed_domains = ['semager.de']
    start_urls = ['http://semager.de/']

    def __init__(self, q='', pause_time=0, word_limit=25, depth=2, *args, **kwargs):
        super(KeywordsSpider, self).__init__(*args, **kwargs)

        try:
            self.pause_time = int(pause_time)

            if self.pause_time < 0:
                self.pause_time = 0
        except ValueError:
            self.pause_time = 0

        try:
            self.word_limit = int(word_limit)

            if self.word_limit > 25:
                self.word_limit = 25
            elif self.word_limit < 1:
                self.word_limit = 1
        except ValueError:
            self.word_limit = 25

        try:
            self.depth = int(depth)

            if self.depth > 5:
                self.depth = 5
            elif self.depth < 1:
                self.depth = 1
        except ValueError:
            self.depth = 2

        q_str = q.strip()
        q_str = q_str.replace(' ', '+')
        self.start_urls = ['http://www.semager.de/keywords/?q=%s' % q_str]

    def parse(self, response):
        pass
