# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class ScienceDirectSpider(PaperSpider):
    name = 'SpringerLink'
    base_url = 'https://link.springer.com'
    page_count = 1

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                query_params = '?query={}'.format('+'.join(keyword_list))
                query_url = "{}/search".format(self.base_url, query_params)
                yield scrapy.Request(url=query_url, callback=self.parse, cb_kwargs=dict(query_params=query_params))

    def parse(self, response, query_params):
        paper_selector_list = response.xpath(".//ol[@id='results-list']//li")
        for paper_selector in paper_selector_list:
            l = ItemLoader(Paper(), selector=paper_selector)
            l.add_xpath('title', './/h2/a//text()', Join(''))
            l.add_value('publisher_url', self.base_url +
                        paper_selector.xpath('.//h2/a/@href').get())
            paper_item = l.load_item()
            yield self.parse_abstract(paper_item)
        self.page_count = self.page_count + 1
        yield response.follow('{}/search/page/{}{}'.format(self.base_url, self.page_count, query_params),
                                callback=self.parse, cb_kwargs=dict(query_params=query_params))