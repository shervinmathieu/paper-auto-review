# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class IEEEXploreSpider(PaperSpider):
    name = 'IEEEXplore'
    base_url = 'https://ieeexplore.ieee.org'
    page_count = 1
    headers = dict({
        'Content-Type': 'application/json',
        'Origin': 'https://ieeexplore.ieee.org'
    })

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                body = dict({
                    'queryText': ' '.join(keyword_list),
                    'rowsPerPage': '100',
                    'pageNumber': self.page_count
                })
                yield scrapy.Request(url='{}/rest/search'.format(self.base_url), method='POST', headers=self.headers,
                                     body=json.dumps(body), callback=self.parse, cb_kwargs=dict(body=body))

    def parse(self, response, body):
        data = json.loads(response.text)
        if data['records'] is not None:
            for record in data['records']:
                l = ItemLoader(Paper())
                l.add_value('title', record['articleTitle'])
                l.add_value('publisher_url', self.base_url +
                            record['documentLink'])
                paper_item = l.load_item()
                yield self.parse_abstract(paper_item)
            self.page_count = self.page_count + 1
            body['pageNumber'] = self.page_count
            yield scrapy.Request(url='{}/rest/search'.format(self.base_url), method='POST', headers=self.headers,
                                 body=json.dumps(body), callback=self.parse, cb_kwargs=dict(body=body))
