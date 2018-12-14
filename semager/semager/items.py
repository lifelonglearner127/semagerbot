# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class TakeLast(object):

    def __call__(self, values):
        for value in reversed(values):
            if value is not None and value != '':
                return value


def filter_percentage(value):
    if value is not None:
        value = value.replace('%', '')
        return round(float(value)/100.0, 4)


class ChildItem(scrapy.Item):
    parent = scrapy.Field(output_processor=TakeLast())
    child = scrapy.Field(output_processor=TakeLast())
    relation = scrapy.Field(input_processor=MapCompose(filter_percentage),
                            output_processor=TakeLast())
    depth = scrapy.Field(output_processor=TakeLast())
    date = scrapy.Field(output_processor=TakeLast())


class FollowedByItem(scrapy.Item):
    parent = scrapy.Field(output_processor=TakeLast())
    followed_by = scrapy.Field(output_processor=TakeLast())
    rank = scrapy.Field(output_processor=TakeLast())
    depth = scrapy.Field(output_processor=TakeLast())
    date = scrapy.Field(output_processor=TakeLast())


class LedByItem(scrapy.Item):
    parent = scrapy.Field(output_processor=TakeLast())
    led_by = scrapy.Field(output_processor=TakeLast())
    rank = scrapy.Field(output_processor=TakeLast())
    depth = scrapy.Field(output_processor=TakeLast())
    date = scrapy.Field(output_processor=TakeLast())


class CategoryItem(scrapy.Item):
    parent = scrapy.Field(output_processor=TakeLast())
    category = scrapy.Field(output_processor=TakeLast())
    likelihood = scrapy.Field(input_processor=MapCompose(filter_percentage),
                              output_processor=TakeLast())
    depth = scrapy.Field(output_processor=TakeLast())
    date = scrapy.Field(output_processor=TakeLast())
