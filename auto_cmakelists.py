#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cuiyiwork@foxmail.com
# Created Time: 21/2/2019 2:09 PM
import os
import sys
import re
from pathlib import Path

str_template = """
CMAKE_MINIMUM_REQUIRED(VERSION 3.0.2)
SET(CMAKE_CXX_STANDARD 11)
PROJECT(%s)
include_directories(
.
%s
)
"""

ptn_src = re.compile("^[-a-zA-Z0-9_]+\.(c|cc|cpp|ipp)$")

input_path = os.path.abspath(sys.argv[1])
if input_path.endswith("/"):
    input_path = input_path[:-1]


current_path = ""
includes = []


def cc_library(**kwargs):
    for include in kwargs.get("includes"):
        rel_inc = current_path if "." == include else include
        includes.append(os.path.join(current_path, rel_inc).replace(input_path + "/", ""))


dict_func = {
    "cc_library": cc_library,
    "glob": Path().glob,
}

list_srcs = []
for root, dirs, files in os.walk(input_path):
    current_path = root
    for file1 in files:
        if file1 in ("BUILD", "BUILD.bazel"):
            execfile(file1, dict_func)
        elif ptn_src.match(file1):
            list_srcs.append(os.path.join(root, file1).replace(input_path + "/", ""))

workspace = os.path.basename(input_path)
list_var = []
final_str = str_template % (workspace, "\n".join(includes))
# for i, srcs in enumerate(list_srcs):
#     final_str += "aux_source_directory(. SRCS%s)\n" % i
#     list_var.append("${SRCS%s}" % i)
final_str += "add_executable(%s %s)" % (workspace, "\n".join(list_srcs))
print(final_str)
