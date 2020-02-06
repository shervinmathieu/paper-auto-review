# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst


class PaperSpider(scrapy.Spider):
    allowed_domains = ['scholar.google.com', 'ieeexplore.ieee.org', 'onlinelibrary.wiley.com', 'link.springer.com', 'sciencedirect.com',
                       'arxiv.org', 'dl.acm.org', 'academic.oup.com', 'oro.open.ac.uk', 'journals.sagepub.com', 'tandfonline.com', 'dl.gi.de',
                       'ncbi.nlm.nih.gov']

    def parse_abstract(self, paper_item):
        publisher_url = str(paper_item['publisher_url'])
        try:
            domain = re.search(r'//(.+?)/', publisher_url).group(1)
            if 'ieeexplore.ieee.org' in domain:
                callback = self.parse_ieeexplore
            elif 'onlinelibrary.wiley.com'in domain:
                callback = self.parse_wiley_library
            elif 'link.springer.com'in domain:
                callback = self.parse_springer
            elif 'sciencedirect.com'in domain:
                callback = self.parse_science_direct
            elif 'arxiv.org'in domain:
                callback = self.parse_arxiv
            elif 'dl.acm.org' in domain:
                callback = self.parse_acm_library
            elif 'academic.oup.com'in domain:
                callback = self.parse_oxford_academic
            elif 'oro.open.ac.uk'in domain:
                callback = self.parse_open_university
            elif 'journals.sagepub.com' in domain or 'tandfonline.com' in domain:
                callback = self.parse_sage_taylor
            elif 'dl.gi.de' in domain:
                callback = self.parse_gesellschaft
            elif 'ncbi.nlm.nih.gov' in domain:
                callback = self.parse_pmc
            else:
                return paper_item
            return scrapy.Request(publisher_url,
                                  callback,
                                  cb_kwargs=dict(paper_item=paper_item))
        except AttributeError:
            return paper_item

    # ieeexplore.ieee.org
    def parse_ieeexplore(self, response, paper_item):
        pattern = re.compile(
            r'global\.document\.metadata=({.*?});', re.MULTILINE | re.DOTALL)
        data = response.xpath(
            "//script[contains(., 'global.document.metadata')]/text()").re(pattern)[0]
        data_obj = json.loads(data)
        l = ItemLoader(item=paper_item)
        l.add_value('abstract', data_obj['abstract'])
        item = l.load_item()
        yield item

    # academic.oup.com
    def parse_oxford_academic(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', "//section[@class='abstract']//text()", Join(''))
        item = l.load_item()
        yield item

    # oro.open.ac.uk
    def parse_open_university(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', ".//h2[contains(text(), 'Abstract')]/following-sibling::p//text()", Join())
        item = l.load_item()
        yield item

    # journals.sagepub.com | tandfonline.com
    def parse_sage_taylor(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_css('abstract', '.abstractInFull p ::text', Join())
        item = l.load_item()
        yield item

    # onlinelibrary.wiley.com
    def parse_wiley_library(self, response, paper_item):
        l=ItemLoader(item=paper_item, response=response)
        l.add_css('abstract', '.article-section__abstract p ::text', Join(''))
        item=l.load_item()
        yield item

    # link.springer.com
    def parse_springer(self, response, paper_item):
        l=ItemLoader(item=paper_item, response=response)
        l.add_css('abstract', '.Abstract p ::text', Join(''))
        item=l.load_item()
        yield item

    # sciencedirect.com
    def parse_science_direct(self, response, paper_item):
        l=ItemLoader(item=paper_item, response=response)
        l.add_css('abstract', '.abstract div ::text', Join(''))
        item=l.load_item()
        yield item

    # dl.acm.org
    def parse_acm_library(self, response, paper_item):
        l=ItemLoader(item=paper_item, response=response)
        l.add_css('abstract', '.article__abstract p ::text', Join(''))
        item=l.load_item()
        yield item

    # dl.gi.de
    def parse_gesellschaft(self, response, paper_item):
        l=ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', ".//h5[contains(text(), 'Abstract')]/following-sibling::div//text()", Join(''))
        item=l.load_item()
        yield item

    # www.ncbi.nlm.nih.gov
    def parse_pmc(self, response, paper_item):
        l=ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', ".//h2[contains(text(), 'Abstract')]/following-sibling::div//text()", Join(''))
        item=l.load_item()
        yield item

    # arxiv.org
    def parse_pmc(self, response, paper_item):
        l=ItemLoader(item=paper_item, response=response)
        l.add_css('abstract', '.abstract ::text', Join(''))
        item=l.load_item()
        yield item
