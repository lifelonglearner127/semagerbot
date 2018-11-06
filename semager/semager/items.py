# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChildItem(scrapy.Item):
    parent = scrapy.Field()
    child = scrapy.Field()
    relation = scrapy.Field()
    depth = scrapy.Field()
    date = scrapy.Field()


class FollowedByItem(scrapy.Item):
    parent = scrapy.Field()
    followed_by = scrapy.Field()
    rank = scrapy.Field()
    depth = scrapy.Field()
    date = scrapy.Field()


class LedByItem(scrapy.Item):
    parent = scrapy.Field()
    led_by = scrapy.Field()
    rank = scrapy.Field()
    depth = scrapy.Field()
    date = scrapy.Field()


class CategoryItem(scrapy.Item):
    parent = scrapy.Field()
    category = scrapy.Field()
    likelihood = scrapy.Field()
    depth = scrapy.Field()
    date = scrapy.Field()
