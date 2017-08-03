#!/usr/bin/env python
# -*- coding: utf-8 -*-



def longest_pub_substr(str1, str2, len_max=10):
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


