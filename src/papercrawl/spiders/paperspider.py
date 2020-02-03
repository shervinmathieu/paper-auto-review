# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst


class PaperSpider(scrapy.Spider):
    allowed_domains = ['ieeexplore.ieee.org', 'academic.oup.com',
                       'oro.open.ac.uk', 'journals.sagepub.com', 'onlinelibrary.wiley.com']

    def parse_abstract(self, paper_item):
        publisher_url = str(paper_item['publisher_url'])
        try:
            domain = re.search(r'//(.+?)/', publisher_url).group(1)
            if domain == 'ieeexplore.ieee.org':
                callback = self.parse_ieeexplore
            elif domain == 'academic.oup.com':
                callback = self.parse_oxford_academic
            elif domain == 'oro.open.ac.uk':
                callback = self.parse_oxford_academic
            elif domain == 'journals.sagepub.com':
                callback = self.parse_sage_journals
            elif domain == 'onlinelibrary.wiley.com':
                callback = self.parse_wiley_library
            else:
                return paper_item
            return scrapy.Request(publisher_url,
                                  callback,
                                  cb_kwargs=dict(paper_item=paper_item))
        except AttributeError:
            return paper_item

    # ieeexplore.ieee.org
    def parse_ieeexplore(self, response, paper_item):
        pattern = re.compile(
            r'global\.document\.metadata=({.*?});', re.MULTILINE | re.DOTALL)
        data = response.xpath(
            "//script[contains(., 'global.document.metadata')]/text()").re(pattern)[0]
        data_obj = json.loads(data)
        l = ItemLoader(paper_item)
        l.add_value('abstract', data_obj['abstract'])
        item = l.load_item()
        yield item

    # academic.oup.com
    def parse_oxford_academic(self, response, paper_item):
        l = ItemLoader(paper_item, response)
        l.add_xpath(
            'abstract', "//section[@class='abstract']//text()", Join(''))
        item = l.load_item()
        yield item

    # oro.open.ac.uk
    def parse_open_university(self, response, paper_item):
        l = ItemLoader(paper_item, response)
        l.add_xpath(
            'abstract', ".//h2[contains(text(), 'Abstract')]/following::p/text()", TakeFirst())
        item = l.load_item()
        yield item

    # journals.sagepub.com
    def parse_sage_journals(self, response, paper_item):
        l = ItemLoader(paper_item, response)
        l.add_xpath(
            'abstract', "//div[@class='abstractSection abstractInFull']//text()")
        item = l.load_item()
        yield item

    # onlinelibrary.wiley.com
    def parse_wiley_library(self, response, paper_item):
        selector = response.css('.article-section__abstract')[0]
        l = ItemLoader(paper_item, selector)
        l.add_xpath('abstract', ".//p/text()")
        item = l.load_item()
        yield item
