#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 14:32:49 2021

@author: swallan
"""

from mpmath import gamma, pi, erf, exp, sqrt, quad, inf, mpf
from mpmath import npdf as phi
from mpmath import ncdf as Phi
from mpmath import mp


def _cdf_mp(q, k, nu, method, verbose=True, error=True, dps=15):
    mp.dps = dps
    q, k, nu = mpf(q), mpf(k), mpf(nu)

    def inner(s, z):
        return phi(z)*(Phi(z+q*s)-Phi(z))**(k-1)

    def outer(s, z):
        return s**(nu-1)*phi(sqrt(nu)*s)*inner(s, z)

    def whole(s, z):
        return sqrt(2*pi)*k*nu**(nu/2) / (gamma(nu/2)*2**(nu/2-1))*outer(s, z)
    res = quad(whole, [0, inf], [-inf, inf], error=error,
               method=method, maxdegree=10)
    return res

def cdf_mp_gl(q, k, nu, verbose=True, error=True, dps=15):
    return _cdf_mp(q, k, nu, method='gauss-legendre', verbose=verbose,
                  error=error, dps=dps)

import srd
import ctypes
from scipy._lib._ccallback import LowLevelCallable
import numpy as np
import scipy.integrate as integrate


def cython_cdf(q, k, v):
    # atol = 10**-(dps)
    usr_data = np.array([q, k, v], float).ctypes.data_as(ctypes.c_void_p)
    llc = LowLevelCallable.from_cython(srd,
                                    "genstudentized_range_cdf",
                                    usr_data)
    ranges = [(-np.inf, np.inf), (0, np.inf)]
    opts = dict(epsabs=10e-14)
    res = integrate.nquad(llc, ranges=ranges, opts=opts)[0]
    return res
    
from statsmodels.stats.libqsturng import psturng
def statsmodels_cdf(q, k, v):
  # `psturng` return the `alpha` value, which we 
  # convert to a `pvalue`. 
  return 1 - psturng(q, k, v)


# number of combinations:
n = int(100 ** (1/3))

qs = (np.random.rand(n) ** 5 + .001) * 1000
qs = np.unique(qs)
ks = ((np.random.rand(n) ** 5 )* 100000).astype(int) % 100 + 2
vs = np.unique(ks)
vs = ((np.random.rand(n) ** 5) * 100000).astype(int) % 100 + 2
vs = np.unique(vs)

from itertools import combinations, product
combinations =list(product(qs, ks, vs))

import json
with open("combinations.txt", "w+") as f:
    f.write(str(combinations))
    
results_cython = dict()
results_mpmath = dict()
results_statsmodels = dict()
    
for q, k, v in combinations:
    print(f"{q} - {k} - {v}")
    results_cython[f"{q}-{k}-{v}"] = cython_cdf(q, k, v)
    # results_mpmath[f"{q}-{k}-{v}"] = cdf_mp_gl(q, float(k), float(v))
    # results_statsmodels[f"{q}-{k}-{v}"] = statsmodels_cdf(q, k, v)

with open("mapmathres.txt", "w+") as f:
    f.write(json.dumps(results_cython))    
    
    

