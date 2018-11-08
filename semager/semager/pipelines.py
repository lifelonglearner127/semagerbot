# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
from semager.items import ChildItem, FollowedByItem, LedByItem, CategoryItem


class SemagerPipeline(object):

    file1_fieldnames = ['parent', 'Child', 'Relation', 'N', 'Date']
    file2_fieldnames = ['parent', 'Followed_by', 'Rank', 'N', 'Date']
    file3_fieldnames = ['parent', 'Led by', 'Rank', 'N', 'Date']
    file4_fieldnames = ['parent', 'category', 'likelihood', 'N', 'Date']


    def open_spider(self, spider):

        if os.path.exists('semager1.csv'):
            self.file1 = open('semager1.csv', 'a', newline='')
        else:
            self.file1 = open('semager1.csv', 'w', newline='')
            writer = csv.DictWriter(self.file1, fieldnames=self.file1_fieldnames)
            writer.writeheader()

        if os.path.exists('semager2.csv'):
            self.file2 = open('semager2.csv', 'a', newline='')
        else:
            self.file2 = open('semager2.csv', 'w', newline='')
            writer = csv.DictWriter(self.file2, fieldnames=self.file2_fieldnames)
            writer.writeheader()

        if os.path.exists('semager3.csv'):
            self.file3 = open('semager3.csv', 'a', newline='')
        else:
            self.file3 = open('semager3.csv', 'w', newline='')
            writer = csv.DictWriter(self.file3, fieldnames=self.file3_fieldnames)
            writer.writeheader()

        if os.path.exists('semager4.csv'):
            self.file4 = open('semager4.csv', 'a', newline='')
        else:
            self.file4 = open('semager4.csv', 'w', newline='')
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
                'parent': item['parent'],
                'Child': item['child'],
                'Relation': item['relation'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
        elif isinstance(item, FollowedByItem):
            writer = csv.DictWriter(self.file2, self.file2_fieldnames)
            writer.writerow({
                'parent': item['parent'],
                'Followed_by': item['followed_by'],
                'Rank': item['rank'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
        elif isinstance(item, LedByItem):
            writer = csv.DictWriter(self.file3, self.file3_fieldnames)
            writer.writerow({
                'parent': item['parent'],
                'Led by': item['led_by'],
                'Rank': item['rank'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
        elif isinstance(item, CategoryItem):
            writer = csv.DictWriter(self.file4, self.file4_fieldnames)
            writer.writerow({
                'parent': item['parent'],
                'category': item['category'],
                'likelihood': item['likelihood'],
                'N': item['depth'],
                'Date': item['date']
            })
            return item
