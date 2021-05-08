#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 18:18:10 2021

@author: swallan
"""

import srd
import ctypes
from scipy._lib._ccallback import LowLevelCallable
import numpy as np
import scipy.integrate as integrate

usr_data = np.array([4.577, 10, 10], float).ctypes.data_as(ctypes.c_void_p)
# usr_data = np.array([3.77, 3, 12], float).ctypes.data_as(ctypes.c_void_p)
llc = LowLevelCallable.from_cython(srd,
                                    "genstudentized_range_cdf",
                                    usr_data)
#%%
def cython_cdf(dps):
    atol = 10**-(dps)
    
    ranges = [(-np.inf, np.inf), (0, np.inf)]
    opts = dict(epsabs=atol)
    res = integrate.nquad(llc, ranges=ranges, opts=opts)[0]
    print(atol)
    print(res)
    return res
    # return integrate.dblquad(llc, -np.inf, np.inf, gfun=0, hfun=np.inf,
    #                                 epsabs=atol)
dps_range = range(5, 25)
# q, k, v = 3.77, 3, 12

cython = []
for dps in dps_range:
    # print(dps)
    cython.append(cython_cdf(dps=dps))
    
"""
cython = 
[0.9410384185385473,
  0.9410384176073167,
  0.9410384176096578,
  0.9410384176099432,
  0.9410384176097508,
  0.9410384176097785,
  0.9410384176097786,
  0.9410384176097786,
  0.9410384176097786,
  0.9410384176097787,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785,
  0.9410384176097785]

"""
#%%
