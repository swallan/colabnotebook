#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 19:40:51 2021

@author: swallan
"""

from mpmath import mp, mpf
import numpy as np
import json

with open("mpmath_res_final.txt", "r") as f:
    gl = json.loads(f.readlines()[0])
    
# with open("sm_res.txt", "r") as f:
#     sm = json.loads(f.readlines()[0])
    
with open("cython_res_final.txt", "r") as f:
    cython = json.loads(f.readlines()[0])



gl_l = []
# sm_l = []
c_l = []

for key in gl.keys():
    if key[0] != "-":
        gl_l.append(mpf(gl[key]))
        # sm_l.append(sm[key])
        c_l.append(float(cython[key]))
  
gl_l = np.asarray(gl_l)
# sm_l = np.asarray(sm_l)
c_l = np.asarray(c_l)

cython_errors = np.asarray(np.abs(c_l - gl_l), dtype=float)
# sm_errors = np.abs(sm_l - gl_l)

import scipy.stats as stats
CI = .99
res_cython = stats.bootstrap((cython_errors,), np.mean, confidence_level=.99)
ci_cython = res_cython.confidence_interval
             
print(f""" Results: \n\n
        Cython {CI} Confidence Interval:
        ---------------------------------
             Lower     |     Upper
          -----------------------------
           {ci_cython.low:.3e}   |    {ci_cython.high:.3e}
      """)