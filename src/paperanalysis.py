import json
import os
import sys
from os.path import expanduser
from abstracttextrank import AbstractTextRank


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
        filtered_list = list()
        for x in os.listdir(output_directory):
            with open('{}/{}'.format(output_directory, x)) as json_file:
                data = json.load(json_file)
                filtered_list.extend(
                    filter(lambda d: not 'abstract' in d, data))
                filtered_data = filter(lambda d: 'abstract' in d, data)
                for data in filtered_data:
                    if data['title'] not in result_title_set:
                        if tr.analyze(data['title'], data['abstract'], window_size=4, lowercase=True):
                            text_rank_keywords = tr.get_keywords(10)
                            text_rank_score = 0
                            for keyword in keywords:
                                if keyword in text_rank_keywords:
                                    text_rank_score = text_rank_score + text_rank_keywords[keyword]
                            data['keywords'] = list(text_rank_keywords.keys())
                            data['score'] = text_rank_score
                            result_title_set.add(data['title'])
                            result_list.append(data)
                        else:
                            if data['abstract'] not in result_title_set:
                                del data['abstract']
                            filtered_list.append(data)
        result_list.sort(key=lambda x: x['score'], reverse=True)
        with open('{}/results.json'.format(result_directory), mode='w', encoding='utf-8') as results_file:
            json.dump(result_list, results_file, ensure_ascii=False, indent=4)
        with open('{}/filtered.json'.format(result_directory), mode='w') as filtered_file:
            json.dump(filtered_list, filtered_file,
                      ensure_ascii=False, indent=4)
