#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import numpy as np


def eigence(np_array):
    mean_arr = np.mean(np_array, axis=0)
    cov_arr = np.cov(np_array - mean_arr)
    # return eigenvalues, eigenvectors
    return np.linalg.eig(np.mat(cov_arr))


def longest_pub_substr(str1, str2, len_max=10):
    if len(str1) > len_max or len(str2) > len_max:
        return ""
    record_table = [[0] * len_max] * len_max

    p = 0
    maxlen = 0
    for i in range(len(str1)):
        for j in range(len(str2)):
            if str1[i] == str2[j]:
                record_table[i + 1][j + 1] = record_table[i][j] + 1
                if record_table[i + 1][j + 1] > maxlen:
                    maxlen = record_table[i + 1][j + 1]
                    p = i + 1

    return str1[maxlen - p: p]


class PatternExtractor(object):
    pattern = None
    __list_part = list()

    def __init__(self, str_pattern):
        """
        /$x/

        The intro below is already invalid
        :param str_pattern: /$num/ means the argument, eg:
            pattern: "/$1/love/$2/"
            string: "I love the water"
            then the result will come out like:
                $1: "I "
                $2: " the water"
        """
        len_x = len("/$x/")
        len_pattern = len(str_pattern)
        idx = str_pattern.find("/$x/")
        if -1 == idx:
            raise StandardError("There is no slot '/$x/' in the pattern")
        if 0 == idx:
            self.__list_part.append("/$x/")
        else:
            self.__list_part.append(str_pattern[: idx])
        pos = idx + len_x
        while pos < len_pattern:
            idx = str_pattern.find("/$x/", pos)
            if -1 == idx:
                self.__list_part.append(str_pattern[pos:])
                break
            if idx == pos:
                raise StandardError("Consecutive slots '/$x//$x/' are forbidden")
            self.__list_part.append(str_pattern[pos: idx])
            pos = idx + len_x
            self.__list_part.append("/$x/")
        pattern_tmp = str_pattern.replace("/$x/", ".+?")
        if "/$x/" == self.__list_part[-1]:
            pattern_tmp = pattern_tmp[:-1]
        self.pattern = re.compile(pattern_tmp)

    def extract(self, string):
        mch = self.pattern.search(string)
        if not mch:
            return None
        str0 = mch.group()
        pos = 0
        list_rst = list()
        part = ""
        for part in self.__list_part:
            if "/$x/" == part:
                continue
            idx = str0.find(part, pos)
            if pos < idx:
                list_rst.append(str0[pos: idx])
            pos = idx + len(part)
        if "/$x/" == part:
            list_rst.append(str0[pos:])
        return tuple(list_rst)


if __name__ == "__main__":
    xtr = PatternExtractor("对/$x/引起的/$x/有/$x/")
    print "||".join(xtr.extract("芍药苷对由紧张刺激引起的大鼠消化道溃疡有明显的抑制作用<sup>［</sup><sup>7</sup><sup>］</sup>。	6"))
