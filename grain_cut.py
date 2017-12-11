#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(r"/home/cuiyi/wheels/")
import loukou.lexical as ll
from functions import longest_pub_substr

dir_data = r"/home/cuiyi/wheels/data/fined"

path_pos = os.path.join(dir_data, r"fine_grained.txt")
path_pro = os.path.join(dir_data, r"sym_pro.txt")
path_dir = os.path.join(dir_data, r"dir.txt")
path_dp_sym = os.path.join(dir_data, r"dp_sym_dis.txt")
path_indp_sym = os.path.join(dir_data, r"indp_sym.txt")
path_indp_dis = os.path.join(dir_data, r"indp_dis.txt")

dict_pos = {}
list_pos = []
with open(path_pos, "r") as f_in:
    for line in f_in:
        item = line.decode("utf-8").strip()
        dict_pos[item] = 1
        list_pos.append((item, 100, u"pos"))
f_in.close()

list_pro = []
with open(path_pro, "r") as f_in:
    for line in f_in:
        item = line.decode("utf-8").strip()
        list_pro.append((item, 10, u"pro"))
f_in.close()

list_dp_sym = []
with open(path_dp_sym, "r") as f_in:
    for line in f_in:
        item = line.decode("utf-8").strip()
        list_dp_sym.append((item, 10000, u"dep_sym"))
f_in.close()

list_indp_sym = []
with open(path_indp_sym, "r") as f_in:
    for line in f_in:
        item = line.decode("utf-8").strip()
        list_indp_sym.append((item, 500, u"indp_sym"))
f_in.close()

list_indp_dis = []
with open(path_indp_dis, "r") as f_in:
    for line in f_in:
        item = line.decode("utf-8").strip()
        list_indp_dis.append((item, 500, u"indp_dis"))
f_in.close()



db = "db"

list_dictionary = []
# list_dictionary.extend(list_pos)
list_dictionary.extend(list_pro)
list_dictionary.extend(list_dp_sym)
list_dictionary.extend(list_indp_sym)
list_dictionary.extend(list_indp_dis)

dict_pattern = {}
for item in list_dictionary:
    # if item[0] in dict_pattern:
    #     print item[0].encode("utf-8")
    dict_pattern[item[0]] = {}
# exit(0)


list_dir = []
with open(path_dir, "r") as f_in:
    for line in f_in:
        item = line.decode("utf-8").strip()
        list_dir.append((item, 1, u"dir"))
f_in.close()

# list_dictionary.extend(list_dir)


list_all = []
all_entries_sym = r"/home/cuiyi/wheels/data/sym_dis.txt"
with open(all_entries_sym, "r") as f_in:
    for line in f_in:
        list_all.append(line.decode("utf-8").strip().split("\t")[0])
f_in.close()


lk = ll.Lexical()
lk.init_tokenizer_tag(list_dictionary)
cnt = 0

list_check_next = []
list_check = list(list_all)
flag_changed = True
list_raw = []
dict_grain = {}
while flag_changed:
    flag_changed = False
    for item1 in list_check:
        cnt += 1
        # if cnt > 30:
        #     break
        str_tmp = u""
        list_temp1 = [item for item in lk.cut_tag(item1)]

        for item2 in list_temp1:
            if item2.flag != "unknown" and item2.flag != "eng":
                if 0 != len(str_tmp):
                    list_raw.append(str_tmp)
                str_tmp = u""
            else:
                str_tmp += item2.word
        if "unknown" == item2.flag or "eng" == item2.flag:
            if 0 != len(str_tmp):
                list_raw.append(str_tmp)

    list_raw = list(set(list_raw) - set(list_dir))

    for i in xrange(len(list_raw)):
        for j in xrange(1, len(list_raw)):
            pub_str = longest_pub_substr(list_raw[i], list_raw[j], 20)
            if pub_str not in dict_grain:
                dict_grain[pub_str] = 0
            dict_grain[pub_str] += 1


list_sorted = sorted(dict_grain.items(), key=lambda d: d[1], reverse=True)
for t in list_sorted:
    if t[0] in dict_pos:
        continue
    print (u"%s\t%d" % t).encode("utf-8")


db = "db"
