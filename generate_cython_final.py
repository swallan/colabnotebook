#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 18:48:48 2021

@author: swallan
"""

import scipy.stats as stats


with open("all_combinations_final.txt", "r") as f:
    combinations_read = f.readlines()[0]

combinations_str_stripped = (combinations_read
                             .replace("[", "")
                             .replace("]", "")
                             .replace("(", "")
                             .replace(")", "")
                             .replace(",", ""))
x = combinations_str_stripped.split(" ")
combinations = [(float(x[i + 0]), float(x[i + 1]), float(x[i + 2])) for i in range(0, len(x), 3)]


cython_out_dict = dict()


i = 1
for (q, k, v) in combinations[::-1]:
    print(f"computation #{len(combinations) -i}")
    i = i + 1
    cython_out_dict[str((q, k, v))] = str(stats.studentized_range.cdf(q, k, v))
    


import json

with open("mpmath_res_final.txt", "w+") as f:
    f.write(json.dumps(cython_out_dict))