# Copyright (c) 2019 Xu LIANG

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import OrderedDict
import numpy as np
import spacy
from spacy_langdetect import LanguageDetector
from spacy.lang.en.stop_words import STOP_WORDS


class AbstractTextRank():
    """Extract keywords from text"""

    def __init__(self):
        self.d = 0.85  # damping coefficient, usually is .85
        self.min_diff = 1e-5  # convergence threshold
        self.steps = 10  # iteration steps
        self.node_weight = None  # save keywords and its weight
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
        self.candidate_pos=['NOUN', 'PROPN']

    def set_stopwords(self, stopwords):
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = self.nlp.vocab[word]
            lexeme.is_stop = True

    def set_candidate_pos(self, candidate_pos):
        """Set candidate parts of speech"""
        self.candidate_pos = candidate_pos

    def sentence_segment(self, title, abstract, candidate_pos, lowercase):
        """Store those words only in cadidate_pos"""
        sentences = []
        selected_words = []
        for token in title:
            # Store words only with cadidate POS tag
            if token.pos_ in candidate_pos and token.is_stop is False:
                if lowercase is True:
                    selected_words.append(token.lemma_.lower())
                else:
                    selected_words.append(token.lemma_)
        sentences.append(selected_words)
        for sent in abstract.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lowercase is True:
                        selected_words.append(token.lemma_.lower())
                    else:
                        selected_words.append(token.lemma_)
            sentences.append(selected_words)
        return sentences

    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        # this is ignore the 0 element in norm
        g_norm = np.divide(g, norm, where=norm != 0)

        return g_norm

    def get_keywords(self, number=10):
        """Print top number keywords"""
        node_weight = OrderedDict(
            sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        keywords = dict() 
        for i, (key, value) in enumerate(node_weight.items()):
            keywords[key] = value
            if i > number:
                break
        return keywords

    def analyze(self, title, abstract, window_size=4, lowercase=False):
        """Main function to analyze text"""

        # Parse text by spaCy
        title_nlp = self.nlp(title)
        abstract_nlp = self.nlp(abstract)

        if abstract_nlp._.language['language'] != 'en':
            return False

        # Filter sentences
        sentences = self.sentence_segment(
            title_nlp, abstract_nlp, self.candidate_pos, lowercase)  # list of list of words

        # Build vocabulary
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)

        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight

        return True
