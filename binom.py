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
    
from statsmodels.stats.libqsturng import psturng, qsturng
def statsmodels_cdf(q, k, v):
  # `psturng` return the `alpha` value, which we 
  # convert to a `pvalue`. 
  return float(1 - psturng(q, k, v))

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
    
# combinations = []
# np.random.seed(123)
# mp.dps=25
# for q, k, v in combinations:
import scipy.optimize as optimize
def ppf(a, k, nu):

    # from scipy.stats import studentized_range
    def func(q, k, nu):
        return (a - (1 - cython_cdf(q , k, nu )))**2
    return optimize.root(func, 3, args=(k, nu)).x.item()
qs = []
for i in range(10):
    # print(i)
    p = (np.random.rand())
    # if p > .999: 
    #     p = .999
    # if p < .1: 
    #     p = .1
    
    k = int((np.random.rand() ** 8 )* 10000000) % 50 + 1
    v = int((np.random.rand() ** 8) * 10000000) % 50 + 1
    # q = ppf(p, k, v)
    # combinations.append((q, k, v))
    print(k, v)
    # qs.append(q)
    # print(f" {cython_cdf(float(q), float(k), float(v)):.5f} {q} - {k} - {v}:")
    # # results_cython[f"{q}-{k}-{v}"] = cython_cdf(q, k, v)
    # results_mpmath[f"{q}-{k}-{v}"] = str(cdf_mp_gl(q, float(k), float(v))[0 ])
    # # results_statsmodels[f"{q}-{k}-{v}"] = statsmodels_cdf(q, k, v)


# with open("q.txt", "w+") as f:
#     f.write(str(qs)) 
    
# with open("q.txt", "r") as f:
#     d = f.readlines()[0][1:-1].split(",")
#     qs = [float(q) for q in d]

# with open("combinations.txt", "w+") as f:
#     f.write(str(combinations))    
# with open("mp_res.txt", "w+") as f:
#     f.write(json.dumps(results_mpmath))  

# mp = '{"1.0000000010066556-15-2": 0.0011575695184391534, "1.0000000010066556-15-3": 0.0005011723333726064, "1.0000000010066556-15-23": 1.7299597777397242e-05, "1.0000000010066556-15-88": 7.48623180710521e-06, "1.0000000010066556-57-2": 1.0416586923300741e-06, "1.0000000010066556-57-3": 4.7596762290399915e-08, "1.0000000010066556-57-23": 1.3157941462776493e-16, "1.0000000010066556-57-88": 1.1253186761601685e-20, "1.0000000010066556-91-2": 5.971187264689727e-08, "1.0000000010066556-91-3": 9.007133306878e-10, "1.0000000010066556-91-23": 3.347032691504026e-23, "1.0000000010066556-91-88": 2.360711339820337e-31, "1.0000000010066556-76-2": 1.8292464315449985e-07, "1.0000000010066556-76-3": 4.2986229937653634e-09, "1.0000000010066556-76-23": 2.2434461475042637e-20, "1.0000000010066556-76-88": 1.024431265971457e-26, "1.0000136574443357-15-2": 0.0011577016103134306, "1.0000136574443357-15-3": 0.000501236174217368, "1.0000136574443357-15-23": 1.7302453017881496e-05, "1.0000136574443357-15-88": 7.487514419058386e-06, "1.0000136574443357-57-2": 1.041941251019031e-06, "1.0000136574443357-57-3": 4.7612419489525534e-08, "1.0000136574443357-57-23": 1.3165669752352088e-16, "1.0000136574443357-57-88": 1.1260680064151021e-20, "1.0000136574443357-91-2": 5.973225140421343e-08, "1.0000136574443357-91-3": 9.010957975765557e-10, "1.0000136574443357-91-23": 3.350062387440354e-23, "1.0000136574443357-91-88": 2.3631966335185856e-31, "1.0000136574443357-76-2": 1.829820052406813e-07, "1.0000136574443357-76-3": 4.300284272215214e-09, "1.0000136574443357-76-23": 2.245151688728403e-20, "1.0000136574443357-76-88": 1.0253379789089038e-26, "1.1730723754568313-15-2": 0.004050881696721062, "1.1730723754568313-15-3": 0.002053552270935829, "1.1730723754568313-15-23": 0.00011350141278396913, "1.1730723754568313-15-88": 5.33440008224229e-05, "1.1730723754568313-57-2": 1.8878163484163972e-05, "1.1730723754568313-57-3": 1.6431719880272931e-06, "1.1730723754568313-57-23": 1.0670311764853861e-13, "1.1730723754568313-57-88": 2.2440478517615044e-17, "1.1730723754568313-91-2": 2.2203748613073295e-06, "1.1730723754568313-91-3": 8.359246032784401e-08, "1.1730723754568313-91-23": 7.740818148539566e-19, "1.1730723754568313-91-88": 3.835311937003038e-26, "1.1730723754568313-76-2": 5.122206061206759e-06, "1.1730723754568313-76-3": 2.6922989127489894e-07, "1.1730723754568313-76-23": 1.0368271551481185e-16, "1.1730723754568313-76-88": 2.4426268177631227e-22, "473.62371805223194-15-2": 0.9999437185882114, "473.62371805223194-15-3": 0.9999993759913676, "473.62371805223194-15-23": 1.0000000000000009, "473.62371805223194-15-88": 1.0000000000000187, "473.62371805223194-57-2": 0.9999038593370849, "473.62371805223194-57-3": 0.9999986588618789, "473.62371805223194-57-23": 0.9999999999999989, "473.62371805223194-57-88": 1.0000000000000382, "473.62371805223194-91-2": 0.9998892264913575, "473.62371805223194-91-3": 0.9999983515218499, "473.62371805223194-91-23": 1.0000000000000022, "473.62371805223194-91-88": 1.0000000000000342, "473.62371805223194-76-2": 0.9998948900583066, "473.62371805223194-76-3": 0.9999984730561676, "473.62371805223194-76-23": 0.9999999999999989, "473.62371805223194-76-88": 1.000000000000045}'
# mp_data = json.loads(mp)

# for key in mp_data.keys():
#     q, k, v = key.split("-")
#     results_cython[key] = cython_cdf(float(q), float(k), float(v))
#     results_statsmodels[key] = statsmodels_cdf(float(q), float(k), float(v))

# # results = dict()
# # results["results_cython"] = results_cython
# # results["results_mpmath"] = results_mpmath
# # results["results_statsmodels"] = results_statsmodels
# with open("mp_res.txt", "w+") as f:
#     f.write(json.dumps(mp_data))   
# with open("cython_res.txt", "w+") as f:
#     f.write(json.dumps(results_cython))    
# with open("sm_res.txt", "w+") as f:
#     f.write(json.dumps(results_statsmodels))  
    
    
    
    

