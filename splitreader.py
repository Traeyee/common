#!/usr/bin/env python

import linecache
import timeit
import os
import commands

# -------------- main ---------------------
file_test = "/home/intership/corpus/emr.split/1.txt.stc"
file_test2 = "/home/intership/corpus/emr.split/4.txt.stc"
dirpath_test = "/home/intership/corpus/emr.split/"
suffix_test = ".stc"
# -----------------------------------------


class SplitReader(object):
    dir_name = ""
    suffix = ""
    list_files = []
    list_lines = []

    def __init__(self, dir_name, suffix):
        self.dir_name = dir_name
        self.suffix = suffix
        list_raw = []
        root, dirs, files = os.walk(dir_name).next()
        for file1 in files:
            if file1.endswith(suffix):
                list_raw.append(file1)
        self.list_files = [os.path.join(root, item) for item in sorted(list_raw, key=lambda l: l)]
        for item in self.list_files:
            self.list_lines.append(int(commands.getoutput("wc -l " + item).split(" ")[0]))

    def getline(self, no):
        if no <= 0:
            return "Error! Must be larger than 0."
        no_tmp = no
        i = 0
        for item in self.list_lines:
            if no_tmp <= item:
                break
            else:
                no_tmp -= item
            i += 1
        if i >= len(self.list_lines):
            return "No exceeds."
        else:
            return linecache.getline(self.list_files[i], no_tmp)


if __name__ == "__main__":
    f_test = SplitReader(dirpath_test, suffix_test)
    print f_test.getline(10)
    print f_test.getline(4000012)

# for i in range(10):
#     ts = timeit.default_timer()
#     if i % 3 == 0:
#         rst = linecache.getline(file_test, 10 + 2 ** i)
#     else:
#         rst = linecache.getline(file_test2, 10 + 2 ** i)
#     te = timeit.default_timer()
#     print rst
#     print str(te - ts)

