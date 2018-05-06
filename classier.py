#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, math
from collections import Counter


class BayesClassifier(object):
    def __init__(self, iterable):
        self.dict_tag_freq = Counter()
        self.dict_tag_total = 0
        self.dict_tag_word_freq = dict()
        self.dict_word_set = dict()
        """
        Train the model
        :param iterable: every item of it is iterable, too; item[0] is tag
        item[1] is a list, containing the words
        """
        for item in iterable:
            tag = item[0] if isinstance(item[0], unicode) else item[0].decode("utf-8")
            self.dict_tag_freq[tag] += 1.0
            self.dict_tag_total += 1
            dict_added = dict()
            for word in item[1]:
                u_word = word if isinstance(word, unicode) else word.decode("utf-8")
                if u_word in dict_added:
                    continue
                dict_added[u_word] = 1
                self.dict_tag_word_freq.setdefault(tag, Counter())[u_word] += 1
                self.dict_word_set[u_word] = 1

    def get_tag(self, list_words):
        list_tag_prob = list()
        for tag in self.dict_tag_freq:
            dict_added = dict()
            log_prob = math.log(self.dict_tag_freq[tag] / self.dict_tag_total)
            for word in list_words:
                u_word = word if isinstance(word, unicode) else word.decode("utf-8")
                if u_word in dict_added:
                    continue
                dict_added[u_word] = 1
                log_prob += math.log((1 + self.dict_tag_word_freq.get(u_word, 0) / self.dict_tag_freq[tag])
                                     / (self.dict_tag_freq[tag] + len(self.dict_word_set)))
            list_tag_prob.append((tag, log_prob))
        return sorted(list_tag_prob, key=lambda t: t[1])[-1][0]
