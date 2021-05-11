#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:45:38 2021

@author: swallan
"""
from mpmath import gamma, pi, sqrt, quad, inf, mpf, mp
from mpmath import npdf as phi
from mpmath import ncdf as Phi

import numpy as np

def cdf_mp(q, k, nu):
    """Straightforward implementation of studentized range CDF"""
    mp.dps = 18
    q, k, nu = mpf(q), mpf(k), mpf(nu)

    def inner(s, z):
        return phi(z) * (Phi(z + q * s) - Phi(z)) ** (k - 1)

    def outer(s, z):
        return s ** (nu - 1) * phi(sqrt(nu) * s) * inner(s, z)

    def whole(s, z):
        return (sqrt(2 * pi) * k * nu ** (nu / 2)
                / (gamma(nu / 2) * 2 ** (nu / 2 - 1)) * outer(s, z))

    res = quad(whole, [0, inf], [-inf, inf],
               method="gauss-legendre", maxdegree=10)
    return res


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


mpmath_out_dict = dict()


i = 1
for (q, k, v) in combinations[:1]:
    print(f"computation #{i}")
    i = i + 1
    mpmath_out_dict[str((q, k, v))] = str(cdf_mp(q, k, v))
    

mp.dps = 25

import json

with open("mpmath_res_final.txt", "w+") as f:
    f.write(json.dumps(mpmath_out_dict))