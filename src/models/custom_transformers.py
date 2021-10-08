# -*- coding: utf-8 -*-

import copy
from sklearn.feature_extraction.text import CountVectorizer

# Overide CountVectorizer to integrate stemming
class StemmedCountVectorizer(CountVectorizer):
    def __init__(self, stemmer, **kwargs):
        super(StemmedCountVectorizer, self).__init__(**kwargs)
        self.stemmer = stemmer

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (self.stemmer.stem(w) for w in analyzer(doc))

    def get_params(self, deep=True):
        params = super().get_params(deep=deep)
        cp = copy.copy(self)
        cp.__class__ = CountVectorizer
        params.update(CountVectorizer.get_params(cp, deep))
        return params

