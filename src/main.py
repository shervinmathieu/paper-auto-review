#!/usr/bin/env python3
import os
import sys
import re
import spacy
from os.path import expanduser
from datetime import datetime
from prompt_toolkit.shortcuts import message_dialog, radiolist_dialog, input_dialog, checkboxlist_dialog, yes_no_dialog
from datetime import datetime
from queryparser import QueryParser
from crawler import crawl
from paperanalysis import analyse_results
from pdfdownloader import download_pdfs


def is_valid_directory(input):
    return re.match(r'^[a-zA-Z_0-9-]+$', input) is not None


def is_valid_query(input):
    return QueryParser().validate(input)


def search_confirm_message(query):
    message = 'This query will search for the following keyword combinations: \n'
    count = 1
    for keyword_list in query:
        message = message + \
            '    {}) {}\n'.format(count, ' '.join(keyword_list))
        count = count + 1
    message = message + 'Is this okay?'
    return message


def lemmatize_keywords(nlp, keywords):
    keywords = keywords.split()
    result = list()
    for keyword in keywords:
        keyword_nlp = nlp(keyword)
        result.append(keyword_nlp[0].lemma_)
    return result

def analyse_confirm_message(keywords):
    message = 'Your input was lemmatized to the following keywords : \n '
    for keyword in keywords:
        message = message + \
            '{} '.format(keyword)
    message = message + '\nIs this okay?'
    return message

home = expanduser("~")
directory = '{}/Documents/paper-auto-review'.format(home)
if not os.path.isdir(directory):
    try:
        os.mkdir(directory)
    except OSError as e:
        print(e)
        print('Creation of main directory %s failed' % directory)
        sys.exit()

results = radiolist_dialog(
    title='Automated paper systematic review',
    text='What do you want to do ?',
    values=[
        ('search', 'Paper search'),
        ('analysis', 'Search result analysis'),
        ('download', 'Download PDFs')
    ]
).run()

if results == 'search':
    query = input_dialog(
        title='Automated paper systematic review',
        text='Input your desired search query:'
    ).run()
    while query is not None and not is_valid_query(query):
        query = input_dialog(
            title='Automated paper systematic review',
            text='Input your desired search query:\nInvalid query.'
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
        title='Automated paper systematic review',
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
            ('CiteSeerX', 'CiteSeerX')
        ]
    ).run()
    while search_engines is not None and len(search_engines) == 0:
        search_engines = checkboxlist_dialog(
            title='Automated paper systematic review',
            text='Select search engines to crawl.\Select at least one.',
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
                ('CiteSeerX', 'CiteSeerX')
            ]
        ).run()
    if search_engines is None:
        sys.exit()

    directory = input_dialog(
        title='Automated paper systematic review',
        text='Input the output directory name:'
    ).run()
    while directory is not None and not is_valid_directory(directory):
        directory = input_dialog(
            title='Automated paper systematic review',
            text='Input the output directory name:\nInvalid directory name.'
        ).run()
    if directory is None:
        sys.exit()
    directory = '{}_{}'.format(
        directory, datetime.utcnow().strftime('%Y-%m-%d_%X'))
    crawl(directory, search_engines, query)

elif results == 'analysis':
    output_directory = '{}/Documents/paper-auto-review/output/'.format(
        expanduser("~"))
    directories = os.listdir(output_directory)
    if len(directories) == 0:
        message_dialog(
            title='Automated paper systematic review',
            text='No search results present.').run()
        sys.exit()
    keywords = input_dialog(
        title='Automated paper systematic review',
        text='Input your desired keywords to test against.\nPlease provide alternate spellings for increased accuracy:'
    ).run()
    while keywords is not None and len(keywords) == 0:
        keywords = input_dialog(
            title='Automated paper systematic review',
            text='Input your desired keywords:\nEmpty input.'
        ).run()
    if keywords is None:
        sys.exit()
    nlp = spacy.load('en_core_web_sm')
    lemma_keywords = lemmatize_keywords(nlp, keywords)
    confirm = yes_no_dialog(
        title='Automated paper systematic review', text=analyse_confirm_message(lemma_keywords)
    ).run()
    if not confirm:
        sys.exit()
    values = list(map(lambda x: (x, x), directories))
    output_directory = radiolist_dialog(
        title='Automated paper systematic review',
        text='Select output directory to analyse.',
        values=values
    ).run()
    if not output_directory:
        sys.exit()
    directory = input_dialog(
        title='Automated paper systematic review',
        text='Input the results directory name:'
    ).run()
    while directory is not None and not is_valid_directory(directory):
        directory = input_dialog(
            title='Automated paper systematic review',
            text='Input the results directory name:\nInvalid directory name.'
        ).run()
    if directory is None:
        sys.exit()
    directory = '{}_{}'.format(
        directory, datetime.utcnow().strftime('%Y-%m-%d_%X'))
    analyse_results(output_directory, directory, lemma_keywords)

elif results == 'download':
    results_directory = '{}/Documents/paper-auto-review/results/'.format(
        expanduser("~"))
    directories = os.listdir(results_directory)
    if len(directories) == 0:
        message_dialog(
            title='Automated paper systematic review',
            text='No analysis results present.').run()
        sys.exit()
    values = list(map(lambda x: (x, x), directories))
    results_directory = radiolist_dialog(
        title='Automated paper systematic review',
        text='Select results directory to download pdfs from.',
        values=values
    ).run()
    download_pdfs(results_directory)


