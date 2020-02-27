# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class MicrosoftAcademicSpider(PaperSpider):
    name = 'MicrosoftAcademic'
    base_url = 'https://academic.microsoft.com'
    start_count = 0
    headers = dict({
        'Content-Type': 'application/json'
    })

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                body = dict({
                    'query': ' '.join(keyword_list),
                    'queryExpression': '',
                    'filters': [],
                    'skip': 0,
                    'take': 10
                })
                yield scrapy.Request(url='{}/api/search'.format(self.base_url), method='POST', headers=self.headers,
                                     body=json.dumps(body), callback=self.parse, cb_kwargs=dict(body=body))

    def parse(self, response, body):
        data = json.loads(response.text)
        if data['pr'] is not None:
            for item in data['pr']:
                l = ItemLoader(Paper())
                l.add_value('title', item['paper']['dn'])
                l.add_value(
                    'publisher_url', '{}/paper/{}'.format(self.base_url, item['paper']['id']))
                l.add_value('authors', list(map(lambda x: x['dn'], item['paper']['a'])))
                l.add_value('abstract', item['paper']['d'])
                yield l.load_item()
            self.start_count = self.start_count + 10
            body['skip'] = self.start_count
            yield scrapy.Request(url='{}/api/search'.format(self.base_url), method='POST', headers=self.headers,
                                 body=json.dumps(body), callback=self.parse, cb_kwargs=dict(body=body))
