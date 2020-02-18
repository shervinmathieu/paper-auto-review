import os
import sys
import re
from datetime import datetime
from prompt_toolkit.validation import Validator
from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog, checkboxlist_dialog, yes_no_dialog
from datetime import datetime
from queryparser import QueryParser
from crawler import crawl

output_root_directory = '../output'


def is_valid_directory(input):
    return re.match(r'^[a-zA-Z_0-9-]+$', input) is not None


def is_valid_query(input):
    return QueryParser().validate(input)


def search_confirm_message(query):
    message = 'This query will search for the following keyword combinations: \n'
    count = 1
    for keyword_list in query:
        message = message + '    {}) {}\n'.format(count, ' '.join(keyword_list))
        count = count + 1
    message = message + 'Is this okay?'
    return message


directory_validator = Validator.from_callable(
    is_valid_directory,
    error_message="Not a valid directory name.",
    move_cursor_to_end=True,
)

results = radiolist_dialog(
    title='Automated paper systematic review',
    text='What do you want to do ?',
    values=[
        ('search', 'Paper search'),
        ('analysis', 'Search result analysis')
    ]
).run()

if results == 'search':
    query = input_dialog(
        title='Automated paper systematic review',
        text='Please input your desired search query:'
    ).run()
    while query is not None and not is_valid_query(query):
        query = input_dialog(
            title='Automated paper systematic review',
            text='Please input your desired search query:\nInvalid query.'
        ).run()
    if query is None:
        sys.exit()
    query = QueryParser().parse(query)

    confirm = yes_no_dialog(
        title='Automated paper systematic review', text=search_confirm_message(query)
    ).run()
    if not confirm:
        sys.exit()

    search_engines = checkboxlist_dialog(
        title='CheckboxList dialog',
        text='Select search engines to crawl.',
        values=[
            ('ACMLibrary', 'ACM Digital Library'),
            ('arXiv', 'arXiv'),
            ('BASE', 'BASE'),
            ('GoogleScholar', 'Google Scholar'),
            ('IEEEXplore', 'IEEE Xplore Digital Library'),
            ('MicrosoftAcademic', 'Microsoft Academic'),
            ('ScienceDirect', 'Science Direct'),
            ('SpringerLink', 'Springer Link'),
            ('WileyLibrary', 'Wiley Online Library'),
        ]
    ).run()
    while search_engines is not None and len(search_engines) == 0:
        search_engines = checkboxlist_dialog(
            title='CheckboxList dialog',
            text='Select search engines to crawl.\nPlease select at least one.',
            values=[
                ('ACMLibrary', 'ACM Digital Library'),
                ('arXiv', 'arXiv'),
                ('BASE', 'BASE'),
                ('GoogleScholar', 'Google Scholar'),
                ('IEEEXplore', 'IEEE Xplore Digital Library'),
                ('MicrosoftAcademic', 'Microsoft Academic'),
                ('ScienceDirect', 'Science Direct'),
                ('SpringerLink', 'Springer Link'),
                ('WileyLibrary', 'Wiley Online Library'),
            ]
        ).run()
    if search_engines is None:
        sys.exit()

    directory = input_dialog(
        title='Automated paper systematic review',
        text='Please input the output directory name:'
    ).run()
    while directory is not None and not is_valid_directory(directory):
        directory = input_dialog(
            title='Automated paper systematic review',
            text='Please input the output directory name:\nInvalid directory name.'
        ).run()
    if directory is None:
        sys.exit()
    diretory = '{}/{}_{}'.format(output_root_directory,
                                 directory, datetime.utcnow().strftime('%Y-%m-%d_%X'))

    crawl(directory, search_engines, query)

elif results == 'analysis':
    print('todo')
