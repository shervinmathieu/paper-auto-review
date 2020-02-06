# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class ACMLibrarySpider(PaperSpider):
    name = 'ACMLibrary'
    base_url = 'https://dl.acm.org'
    page_count = 0

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                query_url = '{}/action/doSearch?AllField={}&pageSize=100'.format(
                    self.base_url, '+'.join(keyword_list))
                yield scrapy.Request(url=query_url, callback=self.parse, cb_kwargs=dict(query_url=query_url), dont_filter=True)

    def parse(self, response, query_url):
        paper_selector_list = response.css('.issue-item__content')
        if len(paper_selector_list) is not 0:
            for paper_selector in paper_selector_list:
                l = ItemLoader(Paper(), selector=paper_selector)
                l.add_xpath(
                    'title', ".//span[@class='hlFld-Title']/a//text()", Join(''))
                l.add_value('publisher_url', self.base_url +
                            paper_selector.xpath(".//span[@class='hlFld-Title']/a/@href").get())
                paper_item = l.load_item()
                yield self.parse_abstract(paper_item)
            self.page_count = self.page_count + 1
            yield response.follow('{}&startPage={}'.format(response.url, self.page_count), callback=self.parse,
                                  cb_kwargs=dict(query_url=query_url))

# https://onlinelibrary.wiley.com/action/doSearch?AllField=graph+visualisation&startPage=3&pageSize=500