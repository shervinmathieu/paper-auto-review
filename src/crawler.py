import os
import sys
from datetime import datetime
from queryparser import QueryParser
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

output_root_directory = '../output'


def crawl(output_directory, search_engines, keyword_list):
    diretory = '{}/{}'.format(output_root_directory, output_directory)
    print(diretory)
    try:
        os.mkdir(diretory)
    except OSError:
        print('Creation of output directory %s failed' % diretory)
        sys.exit()
    else:
        settings = get_project_settings()
        settings.set('OUTPUT_DIRECTORY', diretory)
        # process = CrawlerProcess(settings)
        # for search_engine in search_engines:
        #     process.crawl(search_engine, keywords_array=keyword_list)
        # process.start()
