# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst


class PaperSpider(scrapy.Spider):
    allowed_domains = ['scholar.google.com', 'ieeexplore.ieee.org', 'onlinelibrary.wiley.com', 'link.springer.com', 'sciencedirect.com',
                       'arxiv.org', 'dl.acm.org', 'base-search.net', 'academic.microsoft.com', 'citeseerx.ist.psu.edu', 'academic.oup.com',
                       'oro.open.ac.uk', 'journals.sagepub.com', 'tandfonline.com', 'dl.gi.de', 'ncbi.nlm.nih.gov']

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
            elif 'dl.acm.org' in domain:
                callback = self.parse_acm_library
            elif 'base-search.net' in domain:
                callback = self.parse_base
            elif 'academic.oup.com'in domain:
                callback = self.parse_oxford_academic
            elif 'citeseerx.ist.psu.edu'in domain:
                callback = self.parse_citeseerx
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
        l.add_value('authors', list(
            map(lambda x: x['name'], data_obj['authors'])))
        l.add_value('pdfUrl', data_obj['pdfUrl'])
        item = l.load_item()
        return item

    # academic.oup.com
    def parse_oxford_academic(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', "//section[@class='abstract']//text()", Join(''))
        item = l.load_item()
        return item

    # oro.open.ac.uk
    def parse_open_university(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', ".//h2[contains(text(), 'Abstract')]/following-sibling::p//text()", Join())
        item = l.load_item()
        return item

    # journals.sagepub.com | tandfonline.com
    def parse_sage_taylor(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_css('abstract', '.abstractInFull p ::text', Join())
        item = l.load_item()
        return item

    # onlinelibrary.wiley.com
    def parse_wiley_library(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_css('authors', '.loa-authors .author-name span::text')
        l.add_xpath('pdf_url', "//meta[@name='citation_pdf_url']/@content")
        l.add_css('abstract', '.article-section__abstract p ::text', Join(''))
        item = l.load_item()
        return item

    # link.springer.com
    def parse_springer(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_xpath('authors', "//a[@data-test='author-name']/text()")
        l.add_value('pdf_url', 'https://' +
                    response.xpath("//a[@class='c-pdf-download__link']/@href").get()[2:])
        l.add_css('abstract', '.Abstract p ::text', Join(''))
        item = l.load_item()
        return item

    # sciencedirect.com
    def parse_science_direct(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        authors = list()
        authors_selector = response.css(".author-group .author")
        for author in authors_selector:
            authors.append(' '.join(author.css(".text ::text").getall()))
        l.add_value('authors', authors)
        l.add_xpath('pdf_url', "//meta[@name='citation_pdf_url']/@content")
        l.add_css('abstract', '.abstract div ::text', Join(''))
        item = l.load_item()
        return item

    # dl.acm.org
    def parse_acm_library(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_css('authors', '.citation .author-name::attr(title)')
        l.add_value('pdf_url', 'https://dl.acm.org/' +
                    response.xpath(".//a[@title='PDF']/@href").get())
        l.add_css('abstract', '.article__abstract p ::text', Join(''))
        item = l.load_item()
        return item

    # base-search.net
    def parse_base(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_css('title', '.link-gruen ::text', Join(''))
        l.add_xpath(
            'authors', ".//div[contains(text(), 'Author:')]/following-sibling::div/span/a[1]/text()")
        l.add_xpath(
            'abstract', ".//div[contains(text(), 'Description:')]/following-sibling::div//text()", Join(''))
        item = l.load_item()
        return item

    # citeseerx.ist.psu.edu
    def parse_citeseerx(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        authors = response.xpath("//div[@id='docAuthors']/text()").get()
        authors = authors.strip().split()
        authors = ' '.join(authors[1:]).split(' , ')
        l.add_value('authors', authors)
        l.add_xpath('abstract', "//div[@id='abstract']/p/text()")
        l.add_value('pdf_url', 'https://citeseerx.ist.psu.edu' +
                    response.xpath("//ul[@id='clinks']//a/@href").get())
        item = l.load_item()
        return item

    # dl.gi.de
    def parse_gesellschaft(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', ".//h5[contains(text(), 'Abstract')]/following-sibling::div//text()", Join(''))
        item = l.load_item()
        return item

    # www.ncbi.nlm.nih.gov
    def parse_pmc(self, response, paper_item):
        l = ItemLoader(item=paper_item, response=response)
        l.add_xpath(
            'abstract', ".//h2[contains(text(), 'Abstract')]/following-sibling::div//text()", Join(''))
        item = l.load_item()
        return item
