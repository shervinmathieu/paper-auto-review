import os
from os.path import expanduser
import sys
from datetime import datetime
from queryparser import QueryParser
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def crawl(output_directory, search_engines, keyword_list):
    home = expanduser("~")
    diretory = '{}/Documents/paper-auto-review/output/{}'.format(home, output_directory)
    try:
        os.mkdir(diretory)
    except OSError as e:
        print(e)
        print('Creation of output directory %s failed' % diretory)
        sys.exit()
    else:
        settings = get_project_settings()
        settings.set('OUTPUT_DIRECTORY', diretory)
        process = CrawlerProcess(settings)
        for search_engine in search_engines:
            process.crawl(search_engine, keywords_array=keyword_list)
        process.start()
