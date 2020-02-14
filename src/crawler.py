import os
import sys
from datetime import datetime
from queryparser import QueryParser
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if len(sys.argv) == 2:
    output_root_directory = '../output'

    # generate keywords from user input
    keywords = ['graph', 'visualisation']
    directory = 'test'

    output_directory = '{}/{}_{}'.format(output_root_directory,
                                        directory, datetime.utcnow().strftime('%Y-%m-%d_%X'))

    parser = QueryParser()
    parser.test()

    # try:
    #     os.mkdir(output_directory)
    # except OSError:
    #     print('Creation of output directory %s failed' % output_directory)
    # else:
    #     settings = get_project_settings()
    #     settings.set('OUTPUT_DIRECTORY', output_directory)
    #     process = CrawlerProcess(settings)
    #     # process.crawl('GoogleScholar', keywords_array=[keywords])
    #     # process.crawl('ScienceDirect', keywords_array=[keywords])
    #     # process.crawl('SpringerLink', keywords_array=[keywords])
    #     # process.crawl('ACMLibrary', keywords_array=[keywords])
    #     # process.crawl('WileyLibrary', keywords_array=[keywords])
    #     # process.crawl('BASE', keywords_array=[keywords])
    #     # process.crawl('arXiv', keywords_array=[keywords])
    #     # process.crawl('IEEEXplore', keywords_array=[keywords])
    #     # process.crawl('MicrosoftAcademic', keywords_array=[keywords])
    #     process.start()
else:
    print('Incorrect arguments')
