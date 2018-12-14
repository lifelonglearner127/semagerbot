# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
from semager.items import ChildItem, FollowedByItem, LedByItem, CategoryItem


class SemagerPipeline(object):

    file1_fieldnames = ['Source', 'Target', 'Weight', 'N', 'Date']
    file2_fieldnames = ['Source', 'Target', 'Rank', 'N', 'Date']
    file3_fieldnames = ['Source', 'Target', 'Rank', 'N', 'Date']
    file4_fieldnames = ['Source', 'Target', 'Weight', 'N', 'Date']


    def open_spider(self, spider):
        file_name = '{}_relation.csv'.format(spider.prefix)
        if os.path.exists(file_name):
            self.file1 = open(file_name, 'a', newline='')
        else:
            self.file1 = open(file_name, 'w', newline='')
            writer = csv.DictWriter(self.file1, fieldnames=self.file1_fieldnames)
            writer.writeheader()

        file_name = '{}_follow.csv'.format(spider.prefix)
        if os.path.exists(file_name):
            self.file2 = open(file_name, 'a', newline='')
        else:
            self.file2 = open(file_name, 'w', newline='')
            writer = csv.DictWriter(self.file2, fieldnames=self.file2_fieldnames)
            writer.writeheader()

        file_name = '{}_lead.csv'.format(spider.prefix)
        if os.path.exists(file_name):
            self.file3 = open(file_name, 'a', newline='')
        else:
            self.file3 = open(file_name, 'w', newline='')
            writer = csv.DictWriter(self.file3, fieldnames=self.file3_fieldnames)
            writer.writeheader()

        file_name = '{}_category.csv'.format(spider.prefix)
        if os.path.exists(file_name):
            self.file4 = open(file_name, 'a', newline='')
        else:
            self.file4 = open(file_name, 'w', newline='')
            writer = csv.DictWriter(self.file4, fieldnames=self.file4_fieldnames)
            writer.writeheader()

    def close_spider(self, spider):
        self.file1.close()
        self.file2.close()
        self.file3.close()
        self.file4.close()

    def process_item(self, item, spider):
        if isinstance(item, ChildItem):
            writer = csv.DictWriter(self.file1, self.file1_fieldnames)
            writer.writerow({
                'Source': item['parent'],
                'Target': item['child'],
                'Weight': item['relation'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
        elif isinstance(item, FollowedByItem):
            writer = csv.DictWriter(self.file2, self.file2_fieldnames)
            writer.writerow({
                'Source': item['parent'],
                'Target': item['followed_by'],
                'Rank': item['rank'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
        elif isinstance(item, LedByItem):
            writer = csv.DictWriter(self.file3, self.file3_fieldnames)
            writer.writerow({
                'Source': item['parent'],
                'Target': item['led_by'],
                'Rank': item['rank'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
        elif isinstance(item, CategoryItem):
            writer = csv.DictWriter(self.file4, self.file4_fieldnames)
            writer.writerow({
                'Source': item['parent'],
                'Target': item['category'],
                'Weight': item['likelihood'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
