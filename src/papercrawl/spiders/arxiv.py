# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, Compose, MapCompose
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class ArXivSpider(PaperSpider):
    name = 'arXiv'
    base_url = 'https://arxiv.org/'
    start_count = 0

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                query_url = '{}/search/?searchtype=all&query={}&size=200'.format(
                    self.base_url, '+'.join(keyword_list))
                yield scrapy.Request(url=query_url, callback=self.parse, cb_kwargs=dict(query_url=query_url), dont_filter=True)

    def parse(self, response, query_url):
        paper_selector_list = response.css(".arxiv-result")
        if len(paper_selector_list) is not 0:
            for paper_selector in paper_selector_list:
                l = ItemLoader(Paper(), selector=paper_selector)
                l.add_css(
                    'title', ".title ::text", MapCompose(lambda x: x.strip()), Join(''))
                l.add_xpath('publisher_url', ".//a[contains(text(), 'arXiv')]/@href")
                l.add_css('abstract', ".abstract-full ::text", Compose(self.formatAbstract), Join(''))
                paper_item=l.load_item()
                yield paper_item
            self.start_count=self.start_count + 200
            yield scrapy.Request(url='{}&start={}'.format(query_url, self.start_count), callback=self.parse,
                                  cb_kwargs = dict(query_url=query_url))

    def formatAbstract(self, abstract):
        abstract = list(map(lambda x: x.strip(), abstract))
        abstract.remove('△ Less')
        return abstract