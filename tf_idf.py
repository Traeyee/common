#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


def BM25(dict_dict, k1=2, b=0.75, keep_intermediate=False):
    dl_total = 0
    for d1 in dict_dict:
        dl_total += len(dict_dict[d1])
    dl_avg = float(dl_total) / len(dict_dict)
    dict_tf = dict()
    dict_idf = dict()
    for d1 in dict_dict:
        dict_tf[d1] = dict()
        K = k1 * (1 - b + b * len(dict_dict[d1]) / dl_avg)
        for w1 in dict_dict[d1]:
            db_tf = dict_dict[d1][w1] * (k1 + 1) / (dict_dict[d1][w1] + K)
            dict_tf[d1][w1] = db_tf
            if w1 not in dict_idf:
                dict_idf[w1] = 0
            dict_idf[w1] += 1

    dict_rt = dict()
    for d1 in dict_tf:
        for w1 in dict_tf[d1]:
            db_idf = math.log(float(len(dict_tf) + 1) / dict_idf[w1])
            db_tf = dict_tf[d1][w1] * db_idf
            if keep_intermediate:
                dict_tf[d1][w1] = (db_tf, dict_tf[d1][w1], db_idf)
            else:
                dict_tf[d1][w1] = db_tf
        dict_rt[d1] = dict_tf[d1].items()

    return dict_rt


def KFZ11(dict_dict, k1=2, b=0.75, keep_intermediate=False):
    """
    如何区分杂质和目标：
    杂质多出现在长文本，因为是胡乱组合出来的
    如果是常见杂质，可以用idf降低权重
    如果是少见杂质，应该用tf降低权重：本身频率
    如何区分少见目标和少见杂质？少见杂质还是会有可能在别的地方出现
    tf: 文本长度可直接放分母，频率直接数
    :param dict_dict:
    :param k1:
    :param b:
    :param keep_intermediate:
    :return:
    """

    dict_rt = dict()
    return dict_rt
