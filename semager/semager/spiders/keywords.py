# -*- coding: utf-8 -*-
import scrapy
import datetime


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
        data = response.xpath('//td[@data-th]')
        parent = response.css('input.query').xpath('@value').extract()

        # Fields related to Table1
        relation = data[0].xpath('.//small/text()').extract()
        relation = relation[:self.word_limit]
        children = data[0].xpath('.//a/text()').extract()
        children = children[:self.word_limit]
        links = data[0].xpath(".//a//@href").extract()
        links = links[:self.word_limit]

        # Fields related to Table2
        followers = data[1].xpath('.//text()').extract()
        followers = followers[:self.word_limit]
        rank = range(1, self.word_limit+1)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fields related to Table3
        leaders = data[2].xpath('.//text()').extract()
        leaders = leaders[:self.word_limit]

        # Fields related to Table4
        table4 = response.xpath("//div[@class='card-block']")[0]
        table4_rows = table4.xpath(".//text()").extract()
        table4_rows1 = table4_rows[::2]
        table4_rows2 = table4_rows[1::2]

        try:
            depth = response.meta['depth']
        except KeyError:
            depth = 0

        for i in range(0, len(links)):
            yield {
                'parent': parent,
                'relation': relation[i],
                'children': children[i],
                'links': links[i],
                'depth': depth,
                'follower': followers[i],
                'rank': rank[i],
                'date': date,
                'leader': leaders[i],
                'table4_1': table4_rows1,
                'table4_2': table4_rows2
            }


        for i in range(0, len(links)):
            yield response.follow(links[i], callback=self.parse)

