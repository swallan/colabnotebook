#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:50:28 2021

@author: swallan
"""
import numpy as np
import scipy.stats as stats

# number of combinations
n = 1000

combinations = []
qs = []
ks = []
vs = []

np.random.seed(123456)

for i in range(n):
    if (i) % 10 == 0:
        print(f"generating number {i+1}")
    k = int(np.random.rand() * 98) + 2
    nu = int(np.random.rand() * 119) + 1
    
    p = np.random.rand()
    q = stats.studentized_range.ppf(p, k, nu)
    
    qs.append(q)
    ks.append(k)
    vs.append(nu)
    print(q, k, nu)
    
combinations = zip(qs, ks, vs)
with open("all_combinations_final.txt", "w+") as f:
    f.write(str(list(combinations)))
    