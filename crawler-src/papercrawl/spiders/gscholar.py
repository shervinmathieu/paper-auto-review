# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from papercrawl.items import Paper
from papercrawl.spiders.paperspider import PaperSpider


class GoogleScholarSpider(PaperSpider):
    name = 'GoogleScholar'
    allowed_domains = ['scholar.google.com', 'ieeexplore.ieee.org']
    start_urls = ['https://scholar.google.com/scholar?q=graph+visualisation']

    def parse(self, response):
        papers = response.css('div.gs_scl')
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

        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
