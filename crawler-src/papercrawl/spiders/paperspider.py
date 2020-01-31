# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.loader import ItemLoader


class PaperSpider(scrapy.Spider):

    def parse_ieeexplore(self, response, paper_item):
        pattern = re.compile(r"global\.document\.metadata=({.*?});", re.MULTILINE | re.DOTALL)
        data = response.xpath("//script[contains(., 'global.document.metadata')]/text()").re(pattern)[0]
        data_obj = json.loads(data)
        l = ItemLoader(paper_item)
        l.add_value('abstract', data_obj['abstract'])
        item = l.load_item()
        yield item
