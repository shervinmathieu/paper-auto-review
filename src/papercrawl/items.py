# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join


class Paper(scrapy.Item):
    title = scrapy.Field(serializer=str, output_processor=TakeFirst())
    abstract = scrapy.Field(serializer=str, output_processor=TakeFirst())
    publisher_url = scrapy.Field(serializer=str, output_processor=TakeFirst())
    full_text_url = scrapy.Field(serializer=str, output_processor=TakeFirst())
