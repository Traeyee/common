# -*- coding: utf-8 -*-

import sys


dict_f = dict()
for line in sys.stdin:
	w = line.strip("\n")
	if w not in dict_f:
		dict_f[w] = 0
	dict_f[w] += 1

for t in sorted(dict_f.items(), key=lambda t: t[1], reverse=True):
	print("%s\t%d" % t)

