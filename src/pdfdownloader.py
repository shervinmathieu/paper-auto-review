import os
import json
import sys
import requests
from os.path import expanduser


def download_pdfs(results_directory_name):
    home = expanduser("~")
    main_directory = '{}/Documents/paper-auto-review/pdfs'.format(home)
    if not os.path.isdir(main_directory):
        try:
            os.mkdir(main_directory)
        except OSError as e:
            print(e)
            print('Creation of main pdfs directory %s failed' % main_directory)
            sys.exit()
    results_directory = '{}/Documents/paper-auto-review/results/{}'.format(
        home, results_directory_name)
    pdfs_directory = '{}/Documents/paper-auto-review/pdfs/{}'.format(
        home, results_directory_name)
    try:
        os.mkdir(pdfs_directory)
    except OSError as e:
        print(e)
        print('Creation of pdfs directory %s failed' % pdfs_directory)
        sys.exit()
    else:
        not_downloaded = list()
        no_pdf_url = list()
        with open('{}/results.json'.format(results_directory)) as json_file:
            json_data = json.load(json_file)
            no_pdf_url.extend(
                filter(lambda d: not 'pdf_url' in d, json_data))
            filtered_data = filter(lambda d: 'pdf_url' in d, json_data)
            for paper in filtered_data:
                r = requests.get(paper['pdf_url'], stream=True)
                if r.headers['Content-Type'] == 'application/pdf':
                    with open('{}/{}.pdf'.format(pdfs_directory,
                                                 ''.join(list(filter(lambda ch: ch not in '?.!/;:',
                                                                     paper['title'])))), 'wb') as f:
                        f.write(r.content)
                else:
                    not_downloaded.append(paper)
        with open('{}/no_pdf_url.json'.format(pdfs_directory), mode='w', encoding='utf-8') as opened_file:
            json.dump(no_pdf_url, opened_file, ensure_ascii=False, indent=4)
        with open('{}/not_downloaded.json'.format(pdfs_directory), mode='w', encoding='utf-8') as opened_file:
            json.dump(not_downloaded, opened_file,
                      ensure_ascii=False, indent=4)
