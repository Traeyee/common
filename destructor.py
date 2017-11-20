# -*- coding: utf-8 -*-

"""
内部处理使用Unicode
"""

import sys

sys.path.append("/home/cuiyi/wheels")
import compatitator

PATH_META_DEFAULT = "/home/cuiyi/wheels/data/fined/dp_sym_dis.txt"
PATH_SYM_DEFAULT = "/home/cuiyi/wheels/data/fined/indp_sym.txt"
PATH_DIS_DEFAULT = "/home/cuiyi/wheels/data/fined/indp_dis.txt"


class Destructor:
    """
    A suffix tree
    """
    list_meta = []
    list_sym = []
    list_dis = []
    trie_meta = {}
    trie_sym = {}
    trie_dis = {}

    def __init__(self, path_meta=PATH_META_DEFAULT,
                 path_sym=PATH_SYM_DEFAULT,
                 path_dis=PATH_DIS_DEFAULT):
        # Read the files
        with open(path_meta, "r") as f_in:
            for line in f_in:
                self.list_meta.append(line.decode("utf-8").split("\t"))
        f_in.close()

        with open(path_sym, "r") as f_in:
            for line in f_in:
                self.list_sym.append(line.decode("utf-8").strip())
        f_in.close()

        with open(path_dis, "r") as f_in:
            for line in f_in:
                self.list_dis.append(line.decode("utf-8").strip())
        f_in.close()

        # Build the tries
        for item in self.list_meta:
            self.add2trie(self.trie_meta, item)

        for item in self.list_sym:
            self.add2trie(self.trie_sym, item)

        for item in self.list_dis:
            self.add2trie(self.trie_dis, item)

    def add2trie(self, trie_name, word):
        trie = trie_name
        for i in range(len(word) - 1, -1, -1):
            if word[i] not in trie:
                trie[word[i]] = {}
            trie = trie[word[i]]
        trie["exist"] = True

    def search_trie(self, trie_name, str0):
        """
        :param trie_name:
        :param str0:
        :return: bool, string
        """
        trie = trie_name
        for i in range(len(str0) - 1, -1, -1):
            if str0[i] in trie:
                trie = trie[str0[i]]
                if "exist" in trie:
                    return True, str0[i:]
            else:
                return False, ""
        return False, ""

    def finest_symdis(self, str0, opt="None", return_flag=False):
        """
        If return_flag is True, return whether the string given is that type
        that you want to know; otherwise return the finest-grained term of
        that string(word)
        :param str0: term word given
        :param opt: filter option: "None": none is filtered; "Symptom": only symptom kept
        "Disease": only disease kept
        :param return_flag: control the return type of the function
        :return: defined by return_flag
        """
        str0 = compatitator.strdecode(str0)
        state, str1 = self.search_trie(self.trie_meta, str0)
        if state:
            if return_flag:
                return True
            return str1
        if opt == "Symptom" or opt == "None":
            state, str1 = self.search_trie(self.trie_sym, str0)
            if state:
                if return_flag:
                    return True
                return str1
        if opt == "Disease" or opt == "None":
            state, str1 = self.search_trie(self.trie_dis, str0)
            if state:
                if return_flag:
                    return True
                return str1
        if return_flag:
            return False
        return str0

if __name__ == "__main__":
    dest = Destructor()
    print dest.finest_symdis("经常夜尿")
    print "db"
