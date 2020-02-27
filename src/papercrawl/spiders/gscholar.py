# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class GoogleScholarSpider(PaperSpider):
    name = 'GoogleScholar'
    base_url = 'https://scholar.google.com'
    start_count = 0

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                query_url = '{}/scholar?q={}'.format(
                    self.base_url, '+'.join(keyword_list))
                yield scrapy.Request(url=query_url, callback=self.parse, cb_kwargs=dict(query_url=query_url))

    def parse(self, response, query_url):
        paper_selector_list = response.css('div.gs_scl')
        if len(paper_selector_list) is not 0:
            for paper_selector in paper_selector_list:
                l = ItemLoader(Paper(), selector=paper_selector)
                l.add_xpath('title', './/h3/a//text()', Join(''))
                l.add_xpath('publisher_url', './/h3/a/@href')
                l.add_xpath('authors', ".//div[@class='gs_a']/a/text()")
                l.add_xpath('pdf_url', ".//div[@class='gs_or_ggsm']/a/@href")
                paper_item = l.load_item()
                yield self.parse_abstract(paper_item)
            self.start_count = self.start_count + 10
            yield scrapy.Request(url='{}&start={}'.format(query_url, self.start_count), callback=self.parse,
                                  cb_kwargs=dict(query_url=query_url))
