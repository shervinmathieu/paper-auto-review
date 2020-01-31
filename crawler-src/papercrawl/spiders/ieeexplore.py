# -*- coding: utf-8 -*-
import scrapy


class IEEExploreSpider(scrapy.Spider):
    name = 'IEEExplore'
    allowed_domains = ['ieeexplore.ieee.org']
    #start_urls = ['https://ieeexplore.ieee.org//']

    def parse(self, response):
        item = response.meta['paper_item']
        yield item
