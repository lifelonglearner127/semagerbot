# -*- coding: utf-8 -*-
import os
import csv
import scrapy
import datetime
from scrapy.loader import ItemLoader
from semager.items import ChildItem, FollowedByItem, LedByItem, CategoryItem
from twisted.internet.error import TimeoutError, TCPTimedOutError


class KeywordsSpider(scrapy.Spider):
    name = 'keywords'
    allowed_domains = ['semager.de']
    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def __init__(self, q='', pause_time=0, word_limit=25, depth=2,
        prefix='semager', *args, **kwargs):

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

        self.prefix = prefix.strip()
        q_str = q.strip()
        q_str_list = q_str.split(',')
        for q in q_str_list:
            query = q.replace(' ', '+')
            self.start_urls.append(
                'http://www.semager.de/keywords/?q=%s' % query
            )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.err_callback,
                meta={'download_timeout': self.pause_time}
            )

    def parse(self, response):
        if response.status != 200:
            return None

        data = response.xpath('//td[@data-th]')
        if not data:
            return None

        parent = response.css('input.query').xpath('@value').extract()

        # Fields related to Table1
        relation = data[0].xpath('.//small/text()').extract()
        if relation is not None and isinstance(relation, list):
            relation = relation[:self.word_limit]
            children = data[0].xpath('.//a/text()').extract()
            children = children[:self.word_limit]
            links = data[0].xpath(".//a//@href").extract()
            links = links[:self.word_limit]

        # Fields related to Table2
        followers = data[1].xpath('.//text()').extract()
        if followers is not None and isinstance(followers, list):
            followers = followers[:self.word_limit]
            rank = range(1, self.word_limit+1)
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fields related to Table3
        leaders = data[2].xpath('.//text()').extract()
        if leaders is not None and isinstance(leaders, list):
            leaders = leaders[:self.word_limit]

        # Fields related to Table4
        table4 = response.xpath("//div[@class='card-block']")[0]
        table4_rows = table4.xpath(".//text()").extract()
        categories = table4_rows[1::2]
        likelihood = table4_rows[::2]

        child_list = ItemLoader(item=ChildItem(), response=response)
        followers_list = ItemLoader(item=FollowedByItem(), response=response)
        leaders_list = ItemLoader(item=LedByItem(), response=response)
        category_list = ItemLoader(item=CategoryItem(), response=response)

        try:
            depth = response.meta['depth']
        except KeyError:
            depth = 0

        for i in range(0, len(links)):
            child_list.add_value('parent', parent)
            child_list.add_value('child', children[i])
            child_list.add_value('relation', relation[i])
            child_list.add_value('depth', depth)
            child_list.add_value('date', date)
            yield child_list.load_item()

        for i in range(0, len(followers)):
            followers_list.add_value('parent', parent)
            followers_list.add_value('followed_by', followers[i])
            followers_list.add_value('rank', rank[i])
            followers_list.add_value('depth', depth)
            followers_list.add_value('date', date)
            yield followers_list.load_item()

        for i in range(0, len(leaders)):
            leaders_list.add_value('parent', parent)
            leaders_list.add_value('led_by', leaders[i])
            leaders_list.add_value('rank', rank[i])
            leaders_list.add_value('depth', depth)
            leaders_list.add_value('date', date)
            yield leaders_list.load_item()

        for i in range(0, len(categories)):
            category_list.add_value('parent', parent)
            category_list.add_value('category', categories[i])
            category_list.add_value('likelihood', likelihood[i])
            category_list.add_value('depth', depth)
            category_list.add_value('date', date)
            yield category_list.load_item()

        for link in links:
            yield response.follow(
                link,
                callback=self.parse,
                errback=self.err_callback,
                meta={'download_timeout': self.pause_time}
            )

    def err_callback(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            if os.path.exists('semager_error.csv'):
                error_log = open('semager_error.csv', 'a', newline='')
                writer = csv.DictWriter(
                    error_log,
                    fieldnames=['url']
                )
            else:
                error_log = open('semager_error.csv', 'w', newline='')
                writer = csv.DictWriter(
                    error_log,
                    fieldnames=['url']
                )
                writer.writeheader()
            self.logger.error('TimeoutError on %s', request.meta['download_latency'])
            writer.writerow({
                'url': request.url
            })
