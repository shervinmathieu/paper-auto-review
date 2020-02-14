import sys
import collections
from itertools import product, chain
from lark import Lark, Transformer, Discard, exceptions, lexer


class QueryParser():

    query_grammar = """
        ?exp: term (OR term)*
        ?term: factor (AND factor)*
        ?factor: KEYWORD | "(" exp ")"
        KEYWORD: ESCAPED_STRING
        AND: "&" | "and" | "AND"
        OR: "|" | "or" | "OR"
        %ignore " "
        %import common.ESCAPED_STRING
    """

    def __init__(self):
        super().__init__()
        self.parser = parser = Lark(self.query_grammar, start='exp')

    def parse(self, query):
        try:
            query_tree = self.parser.parse(query)
            if isinstance(query_tree, lexer.Token):
                if query_tree.type != 'KEYWORD':
                    raise Exception
                return [query_tree[1:-1].split()]
            return QueryTransformer(visit_tokens=True).transform(query_tree)
        except Exception as e:
            print('Query parsing error.')
            sys.exit()

    def validate(self, query):
        try:
            query_tree = self.parser.parse(query)
            return True
        except Exception as e:
            return False

class QueryTransformer(Transformer):
    def KEYWORD(self, arg):
        return [arg[1:-1].split()]

    def AND(self, arg):
        raise Discard

    def OR(self, arg):
        raise Discard

    def exp(self, args):
        return [item for sublist in args for item in sublist]

    def term(self, args):
        result = list()
        for operation in product(*args):
            result.append(list(flatten(operation)))
        return result


def flatten(l):
    for element in l:
        if isinstance(element, collections.Iterable) and not isinstance(element, (str, bytes)):
            yield from flatten(element)
        else:
            yield element
