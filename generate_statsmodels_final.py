#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:12:19 2021

@author: swallan
"""


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


statsmodels_out_dict = dict()

from statsmodels.stats.libqsturng import psturng, qsturng
def statsmodels_cdf(q, k, v):
  # `psturng` return the `alpha` value, which we 
  # convert to a `pvalue`. 
  return float(1 - psturng(q, k, v))

i = 1
for (q, k, v) in combinations:
    print(f"computation #{len(combinations) -i}")
    if (len(statsmodels_out_dict)) != i-1:
        print("bad")
    i = i + 1

    statsmodels_out_dict[str((q, k, v))] = str(statsmodels_cdf(q, k, v))
    


import json

# if len(statsmodels_out_dict) != 999: 
with open("statsmodels_res_final.txt", "w+") as f:
    f.write(json.dumps(statsmodels_out_dict))