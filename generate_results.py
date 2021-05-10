#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 16:51:02 2021

@author: swallan
"""
#%%
from mpmath import mp, mpf
import numpy as np
import json

with open("mp_res.txt", "r") as f:
    gl = json.loads(f.readlines()[0])
    
with open("sm_res.txt", "r") as f:
    sm = json.loads(f.readlines()[0])
    
with open("cython_res.txt", "r") as f:
    cython = json.loads(f.readlines()[0])
    
# gl = dict()


gl_l = []
sm_l = []
c_l = []

for key in gl.keys():
    gl_l.append(mpf(gl[key]))
    sm_l.append(sm[key])
    c_l.append(cython[key])
  
gl_l = np.asarray(gl_l)
sm_l = np.asarray(sm_l)
c_l = np.asarray(c_l)

cython_errors = np.abs(c_l - gl_l)
sm_errors = np.abs(sm_l - gl_l)
             
# cython_count = np.count_nonzero(cython_errors[cython_errors > 10e-8])
# sm_count = np.count_nonzero(sm_errors[sm_errors > 10e-8])
  

count_better_than_sm = np.count_nonzero(np.ones_like(cython_errors)[cython_errors < 10e-10])

from scipy.stats import binom_test

pval = binom_test(count_better_than_sm,
                  len(sm_l),
                  p=.05)
print(f"The results are {'not ' if pval > .05 else ''}significant at the significance level p=.05: p={pval:.5f}")
    
