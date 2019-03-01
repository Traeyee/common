#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cuiyiwork@foxmail.com
# Created Time: 21/2/2019 2:09 PM
import os
import sys
import json
import logging
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
# input_path = os.path.abspath("/home/cuiyi/blade_repos")
if input_path.endswith("/"):
    input_path = input_path[:-1]


current_path = ""
includes = []
list_tmp = []

file_tmp = "/tmp/.auto_cmakelists.tmp"
if os.path.exists(file_tmp):
    os.remove(file_tmp)


def common_func(**kwargs):
    with open(file_tmp, "a") as f:
        incs = []
        for include in kwargs.get("includes", []):
            rel_inc = current_path if "." == include else include
            joint_path = os.path.join(current_path, rel_inc).replace(input_path + "/", "")
            incs.append(joint_path)
        for inc in incs:
            f.write(inc + "\n")
        f.close()


dict_func = {
    "cc_library": common_func,
    "cc_binary": common_func,
    "cc_proto_library": common_func,
    "proto_library": common_func,
    "boost_library": common_func,
    "glob": Path().glob,
    "load": lambda *args: None,
    "config_setting": lambda **kwargs: None,
    "select": lambda *args: None,
}

list_srcs = []
for root, dirs, files in os.walk(input_path):
    current_path = root
    for file1 in files:
        abs_file = os.path.join(root, file1)
        if file1 in ("BUILD", "BUILD.bazel"):
            try:
                execfile(abs_file, dict_func)
            except Exception as e:
                logging.warning(e)
                continue
        elif ptn_src.match(file1):
            list_srcs.append(abs_file.replace(input_path + "/", ""))

workspace = os.path.basename(input_path)
with open(file_tmp, "r") as f:
    for line in f:
        includes.append(line.strip())
    f.close()
final_str = str_template % (workspace, "\n".join(includes))
list_var = []
# for i, srcs in enumerate(list_srcs):
#     final_str += "aux_source_directory(. SRCS%s)\n" % i
#     list_var.append("${SRCS%s}" % i)
final_str += "add_executable(%s %s)" % (workspace, "\n".join(list_srcs))
print(final_str)
