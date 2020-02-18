import os
import sys
from datetime import datetime
from queryparser import QueryParser
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def crawl(output_directory, search_engines, keyword_list):
    try:
        os.mkdir(output_directory)
    except OSError:
        print('Creation of output directory %s failed' % output_directory)
        sys.exit()
    else:
        settings = get_project_settings()
        settings.set('OUTPUT_DIRECTORY', output_directory)
        process = CrawlerProcess(settings)
        for search_engine in search_engines:
            process.crawl(search_engine, keywords_array=keyword_list)
        process.start()
