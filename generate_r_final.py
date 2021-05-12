#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 20:23:35 2021

@author: swallan
"""

import numpy as np
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

qs = []
ks = []
vs = []

for q, k, v in combinations:
    qs.append(q)
    ks.append(k)
    vs.append(v)
    


# run this in the terminal!
#%%
%load_ext rpy2.ipython 
#%%
%%R -o r_out -i qs -i ks -i vs
r_out <- c()
print(length(qs))
upper = length(qs)+1
for (i in 1:length(qs)) { 
    print(ptukey(as.numeric(qs[i]), as.numeric(ks[i]), as.numeric(vs[i])))
    r_out <-c(r_out, ptukey(as.numeric(qs[i]), as.numeric(ks[i]), as.numeric(vs[i])))
    }
#%%
r_out_dict = dict()

for c, r in zip(combinations, r_out):
    r_out_dict[str(c)] = str(r)

import json

# if len(statsmodels_out_dict) != 999: 
with open("r_res_final.txt", "w+") as f:
    f.write(json.dumps(r_out_dict))
    
    
