# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem

class PaperPipeline(object):

    urls_seen = set()

    def __init__(self, output_directory):
        self.output_directory = output_directory

    @classmethod
    def from_crawler(cls, crawler):
        output_directory = crawler.settings.get('OUTPUT_DIRECTORY')
        return cls(output_directory)

    def open_spider(self, spider):
        if self.output_directory is not None:
            file_name = '{}/{}.json'.format(self.output_directory,
                                        spider.name)
            self.file = open(file_name, 'w+b')
            self.exporter = JsonItemExporter(self.file)
            self.exporter.start_exporting()

    def close_spider(self, spider):
        if self.output_directory is not None:
            self.exporter.finish_exporting()
            self.file.close()

    def process_item(self, item, spider):
        if item['publisher_url'] in self.urls_seen:
            raise DropItem('Duplicate item found: %s' % item)
        else:
            self.urls_seen.add(item['publisher_url'])
            if self.output_directory is not None:
                self.exporter.export_item(item)
        return item
