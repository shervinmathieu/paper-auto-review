import os
from os.path import expanduser
import sys
from datetime import datetime
from queryparser import QueryParser
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def crawl(output_directory_name, search_engines, keyword_list):
    home = expanduser("~")
    main_directory = '{}/Documents/paper-auto-review/output'.format(home)
    if not os.path.isdir(main_directory):
        try:
            os.mkdir(main_directory)
        except OSError as e:
            print(e)
            print('Creation of main output directory %s failed' % main_directory)
            sys.exit()
    output_directory = '{}/Documents/paper-auto-review/output/{}'.format(home, output_directory_name)
    try:
        os.mkdir(output_directory)
    except OSError as e:
        print(e)
        print('Creation of output directory %s failed' % output_directory)
        sys.exit()
    else:
        settings = get_project_settings()
        settings.set('OUTPUT_DIRECTORY', output_directory)
        process = CrawlerProcess(settings)
        for search_engine in search_engines:
            process.crawl(search_engine, keywords_array=keyword_list)
        process.start()
