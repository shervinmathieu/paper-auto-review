# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class ScienceDirectSpider(PaperSpider):
    name = 'ScienceDirect'
    base_url = 'https://www.sciencedirect.com'
    start_count = 0

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                url = '{}/search/advanced?qs={}&show=100'.format(
                    self.base_url, '%20'.join(keyword_list))
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        paper_selector_list = response.css('.ResultItem')
        if len(paper_selector_list) is not 0:
            for paper_selector in paper_selector_list:
                l = ItemLoader(Paper(), seletor=paper_selector)
                l.add_xpath('title', './/h2//a//text()', Join(''))
                l.add_value('publisher_url', self.base_url +
                            paper_selector.xpath('.//h2//a/@href').get())
                paper_item = l.load_item()
                yield self.parse_abstract(paper_item)
            self.start_count = self.start_count + 100
            yield response.follow('{}&offset={}'.format(response.url, self.start_count), callback=self.parse)
