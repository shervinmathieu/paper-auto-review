import json
import os
import sys
from os.path import expanduser
from abstracttextrank import AbstractTextRank


def analyse_results(output_directory_name, results_directory_name, keywords):
    home = expanduser("~")
    main_directory = '{}/Documents/paper-auto-review/results'.format(home)
    if not os.path.isdir(main_directory):
        try:
            os.mkdir(main_directory)
        except OSError as e:
            print(e)
            print('Creation of main results directory %s failed' % main_directory)
            sys.exit()
    output_directory = '{}/Documents/paper-auto-review/output/{}'.format(
        home, output_directory_name)
    results_directory = '{}/Documents/paper-auto-review/results/{}'.format(
        home, results_directory_name)
    try:
        os.mkdir(results_directory)
    except OSError as e:
        print(e)
        print('Creation of results directory %s failed' % results_directory)
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
                json_data = json.load(json_file)
                no_abstract.extend(
                    filter(lambda d: not 'abstract' in d, json_data))
                filtered_data = filter(lambda d: 'abstract' in d, json_data)
                for paper in filtered_data:
                    if paper['title'] not in result_title_set:
                        if tr.analyze(paper['title'], paper['abstract'], window_size=4, lowercase=True):
                            text_rank_keywords = tr.get_keywords(10)
                            text_rank_score = 1
                            for keyword in keywords:
                                if keyword in text_rank_keywords:
                                    text_rank_score = text_rank_score * \
                                        text_rank_keywords[keyword]
                            paper['keywords'] = list(text_rank_keywords.keys())
                            result_title_set.add(paper['title'])
                            if text_rank_score == 1:
                                score_is_0.append(paper)
                            else:
                                paper['score'] = text_rank_score
                                result_list.append(paper)
                        else:
                            not_in_english.append(paper)
        result_list.sort(key=lambda x: x['score'], reverse=True)
        with open('{}/results.json'.format(results_directory), mode='w', encoding='utf-8') as opened_file:
            json.dump(result_list, opened_file, ensure_ascii=False, indent=4)
        with open('{}/no_abstract.json'.format(results_directory), mode='w') as opened_file:
            json.dump(no_abstract, opened_file,
                      ensure_ascii=False, indent=4)
        with open('{}/not_in_english.json'.format(results_directory), mode='w') as opened_file:
            json.dump(not_in_english, opened_file,
                      ensure_ascii=False, indent=4)
        with open('{}/score_is_0.json'.format(results_directory), mode='w') as opened_file:
            json.dump(score_is_0, opened_file,
                      ensure_ascii=False, indent=4)
