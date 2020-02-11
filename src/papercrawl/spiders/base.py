# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class BASESpider(PaperSpider):
    name = 'BASE'
    base_url = 'https://www.base-search.net'
    page_count = 0

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                query_url = '{}/Search/Results?lookfor={}&l=en'.format(
                    self.base_url, '+'.join(keyword_list))
                yield scrapy.Request(url=query_url, callback=self.parse, cb_kwargs=dict(query_url=query_url))

    def parse(self, response, query_url):
        paper_selector_list = response.xpath(".//a[contains(text(), 'Detail View')]")
        for paper_selector in paper_selector_list:
            l = ItemLoader(Paper(), selector=paper_selector)
            l.add_value('publisher_url', self.base_url +
                        paper_selector.xpath("./@href").get())
            paper_item = l.load_item()
            yield self.parse_abstract(paper_item)
        if self.page_count < 100:
            self.page_count = self.page_count + 1
            yield scrapy.Request(url='{}&page={}'.format(query_url, self.page_count), callback=self.parse,
                                    cb_kwargs=dict(query_url=query_url))
