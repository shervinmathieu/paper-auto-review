# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class GoogleScholarSpider(PaperSpider):
    name = 'GoogleScholar'
    allowed_domains = ['scholar.google.com', 'ieeexplore.ieee.org']
    base_url = 'https://scholar.google.com'
    start_count = 0

    def __init__(self, keywords_array=None):
        self.keywords_array = keywords_array

    def start_requests(self):
        if self.keywords_array is not None:
            for keyword_list in self.keywords_array:
                url = "{}/scholar?q={}".format(self.base_url, '+'.join(keyword_list))
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        papers = response.css('div.gs_scl')
        if len(papers) is not 0:
            for paper in papers:
                l = ItemLoader(item=Paper(), selector=paper)
                l.add_xpath('title', './/h3/a//text()', Join(''))
                l.add_xpath('publisher_link', './/h3/a/@href', TakeFirst())
                l.add_xpath('full_text_link',
                            ".//div[@class='gs_or_ggsm']/a/@href", TakeFirst())
                paper_item = l.load_item()
                publisher_link_str = str(paper_item['publisher_link'])
                if publisher_link_str.startswith('https://ieeexplore.ieee.org'):
                    yield scrapy.Request(publisher_link_str,
                                        callback=self.parse_ieeexplore,
                                        cb_kwargs=dict(paper_item=paper_item))
                else:
                    yield paper_item
            self.start_count = self.start_count + 10
            yield response.follow("{}&start={}".format(response.url, self.start_count), callback=self.parse)
