import os
import json
import sys
from os.path import expanduser
from abstracttextrank import AbstractTextRank

# import requests
# url='https://pdfs.semanticscholar.org/c029/baf196f33050ceea9ecbf90f054fd5654277.pdf'
# r = requests.get(url, stream=True)
# r.headers['Content-Type'] == application/pdf
# with open('C:/Users/MICRO HARD/myfile.pdf', 'wb') as f:
# f.write(r.content)

def analyse_results(output_directory_name, result_directory_name, keywords):
    output_directory = '{}/Documents/paper-auto-review/output/{}'.format(
        expanduser("~"), output_directory_name)
    result_directory = '{}/Documents/paper-auto-review/results/{}'.format(
        expanduser("~"), result_directory_name)
    try:
        os.mkdir(result_directory)
    except OSError as e:
        print(e)
        print('Creation of results directory %s failed' % result_directory)
        sys.exit()
    else:
        tr = AbstractTextRank()
        tr.set_candidate_pos(['NOUN', 'PROPN', 'VERB', 'ADJ'])
        result_title_set = set()
        result_list = list()
        no_abstract = list()
        not_in_english = list()
        score_is_0 = list()
        for x in os.listdir(output_directory):
            with open('{}/{}'.format(output_directory, x)) as json_file:
                data = json.load(json_file)
                no_abstract.extend(
                    filter(lambda d: not 'abstract' in d, data))
                filtered_data = filter(lambda d: 'abstract' in d, data)
                for data in filtered_data:
                    if data['title'] not in result_title_set:
                        if tr.analyze(data['title'], data['abstract'], window_size=4, lowercase=True):
                            text_rank_keywords = tr.get_keywords(10)
                            text_rank_score = 1
                            for keyword in keywords:
                                if keyword in text_rank_keywords:
                                    text_rank_score = text_rank_score * \
                                        text_rank_keywords[keyword]
                            data['keywords'] = list(text_rank_keywords.keys())
                            result_title_set.add(data['title'])
                            if text_rank_score == 1:
                                score_is_0.append(data)
                            else:
                                data['score'] = text_rank_score
                                result_list.append(data)
                        else:
                            not_in_english.append(data)
        result_list.sort(key=lambda x: x['score'], reverse=True)
        with open('{}/results.json'.format(result_directory), mode='w', encoding='utf-8') as opened_file:
            json.dump(result_list, opened_file, ensure_ascii=False, indent=4)
        with open('{}/no_abstract.json'.format(result_directory), mode='w') as opened_file:
            json.dump(no_abstract, opened_file,
                      ensure_ascii=False, indent=4)
        with open('{}/not_in_english.json'.format(result_directory), mode='w') as opened_file:
            json.dump(not_in_english, opened_file,
                      ensure_ascii=False, indent=4)
        with open('{}/score_is_0.json'.format(result_directory), mode='w') as opened_file:
            json.dump(score_is_0, opened_file,
                      ensure_ascii=False, indent=4)
