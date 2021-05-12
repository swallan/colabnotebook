#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 20:29:12 2021

@author: swallan
"""

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
import numpy as np


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

# import srd
# import ctypes
# from scipy._lib._ccallback import LowLevelCallable
# import numpy as np
# import scipy.integrate as integrate


# def cython_cdf(q, k, v):
#     # atol = 10**-(dps)
#     usr_data = np.array([q, k, v], float).ctypes.data_as(ctypes.c_void_p)
#     llc = LowLevelCallable.from_cython(srd,
#                                     "genstudentized_range_cdf",
#                                     usr_data)
#     ranges = [(-np.inf, np.inf), (0, np.inf)]
#     opts = dict(epsabs=10e-14)
#     res = integrate.nquad(llc, ranges=ranges, opts=opts)[0]
#     return res
    
# from statsmodels.stats.libqsturng import psturng
# def statsmodels_cdf(q, k, v):
#   # `psturng` return the `alpha` value, which we 
#   # convert to a `pvalue`. 
#   return float(1 - psturng(q, k, v))

# number of combinations:
n = int(100 ** (1/3))

qs = (np.random.rand(n * 2) ** 5 + .001) * 150
qs = np.unique(qs)
ks = ((np.random.rand(n) ** 5 )* 100000).astype(int) % 50 + 2
vs = np.unique(ks)
vs = ((np.random.rand(n) ** 5) * 100000).astype(int) % 50 + 2
vs = np.unique(vs)

from itertools import combinations, product
combinations =list(product(qs, ks, vs))


# LOAD IN THE COMBINATIONS

import json
# with open("combinations.txt", "r") as f:
#     r = f.readlines()[0]
# r = r[1:-1].replace("(", "").replace(")", "")
# l = r.split(",")
# ls = [(float(l[i]), float(l[i+1]), float(l[i+2])) for i in range(0, len(l), 3)]

results_cython = dict()
results_mpmath = dict()
results_statsmodels = dict()
    
combinations = []
with open("q.txt", "r") as f:
    d = f.readlines()[0][1:-1].split(",")
    qs = [float(q) for q in d]
    
np.random.seed(123)
mp.dps=25
# for q, k, v in combinations:
for i in range(1000):
    print(i)
    q = qs[i]
    # q = (np.random.rand() ** 5 + .001) * 150
    k = int((np.random.rand() ** 5 )* 100000) % 50 + 2
    v = int((np.random.rand() ** 5) * 100000) % 50 + 2
    combinations.append((q, k, v))
    print(f"{q} - {k} - {v}")
    # results_cython[f"{q}-{k}-{v}"] = cython_cdf(q, k, v)
    results_mpmath[f"{q}-{k}-{v}"] = str(cdf_mp_gl(q, float(k), float(v))[0 ])
    # results_statsmodels[f"{q}-{k}-{v}"] = statsmodels_cdf(q, k, v)

with open("combinations.txt", "w+") as f:
    f.write(str(combinations))    
with open("mp_res.txt", "w+") as f:
    f.write(json.dumps(results_mpmath))  

# results = dict()
# results["results_cython"] = results_cython
# results["results_mpmath"] = results_mpmath
# results["results_statsmodels"] = results_statsmodels

# with open("cython_res.txt", "w+") as f:
#     f.write(json.dumps(results_cython))    
# with open("sm_res.txt", "w+") as f:
#     f.write(json.dumps(results_statsmodels))  
    
    
    
    

