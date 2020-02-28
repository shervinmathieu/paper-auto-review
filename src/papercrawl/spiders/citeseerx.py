# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class CiteSeerXSpider(PaperSpider):
    name = 'CiteSeerX'
    base_url = 'https://citeseerx.ist.psu.edu'
    start_count = 0

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                query_url = '{}/search?q={}'.format(
                    self.base_url, '+'.join(keyword_list))
                yield scrapy.Request(url=query_url, callback=self.parse, cb_kwargs=dict(query_url=query_url))

    def parse(self, response, query_url):
        paper_selector_list = response.css('div.result')
        if len(paper_selector_list) is not 0:
            for paper_selector in paper_selector_list:
                l = ItemLoader(Paper(), selector=paper_selector)
                l.add_css('title', '.doc_details ::text', MapCompose(lambda x: x.strip()), Join(' '))
                l.add_value('publisher_url', self.base_url +
                            paper_selector.css('.doc_details ::attr(href)').get())
                paper_item = l.load_item()
                yield self.parse_abstract(paper_item)
            self.start_count = self.start_count + 10
            yield scrapy.Request(url='{}&start={}'.format(query_url, self.start_count), callback=self.parse,
                                 cb_kwargs=dict(query_url=query_url))
