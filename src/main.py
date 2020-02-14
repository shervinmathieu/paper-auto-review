import os
import sys
import re
from PyInquirer import prompt, print_json
from PyInquirer import Validator, ValidationError
from datetime import datetime
from queryparser import QueryParser


class DirectoryValidator(Validator):
    def validate(self, document):
        valid = re.match(r'^[a-zA-Z_0-9-]+$', document.text) is not None
        if not valid:
            raise ValidationError(
                message='Please enter a valid directory name',
                cursor_position=len(document.text))


class QueryValidator(Validator):
    def validate(self, document):
        valid = QueryParser().validate(document.text)
        if valid is not True:
            raise ValidationError(
                message='Query parsing error. Make sure your query is written correctly.',
                cursor_position=len(document.text))


questions = [
    {
        'type': 'list',
        'name': 'process',
        'message': 'What do you want to do?',
        'choices': [
            {
                'name': 'Automated paper search',
                'value': 'search'
            },
            {
                'name': 'Result analysis',
                'value': 'analysis'
            }
        ]
    },
    {
        'type': 'input',
        'name': 'directory',
        'message': 'Input the output directory name.',
        'validate': DirectoryValidator,
        'when': lambda answers: answers['process'] == 'search'

    },
    {
        'type': 'input',
        'name': 'query',
        'message': 'Input your desired search query.',
        'validate': QueryValidator,
        'filter': lambda input: QueryParser().parse(input),
        'when': lambda answers: answers['process'] == 'search'

    },
    {
        'type': 'checkbox',
        'name': 'search_engines',
        'message': 'Select search engines to crawl.',
        'choices' : [

        ],
        'when': lambda answers: answers['process'] == 'search'

    },
    # {
    #     'type': 'input',
    #     'name': 'output_directory',
    #     'message': 'What\'s your first name',
    # }
]

answers = prompt(questions)
print(answers)

# qs = [
#     # '"a g" | "b" | "c"',
#     # '"a" & "b" | "c"',
#     # '"a" & "b" | "c" & "d" ',
#     # '("a" | "b") | ("c" | "d")',
#     # '"a" & ("b" | "c") & ("d" | "e")',
#     # '("b" & ("c" | "d") | "e" & ("f" | "g"))',
#     # '"a" & ("b" & ("c" | "d") & "e" & ("f" | "g")) | x'
# ]
