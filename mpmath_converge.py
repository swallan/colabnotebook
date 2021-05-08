#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:51:12 2021

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


def cdf_mp_ts(q, k, nu, verbose=True, error=True, dps=15):
    return _cdf_mp(q, k, nu, method='tanh-sinh', verbose=verbose, error=error,
                  dps=dps)


dps_range = range(5, 25)
# q, k, v = 4.577, 10, 10
q, k, v = 3.77, 3, 12
ts_cdf = []
gl_cdf = []
for dps in dps_range:
    print(dps)
    ts_cdf.append(cdf_mp_ts(q, k, v, dps=dps)[0])
    gl_cdf.append(cdf_mp_gl(q, k, v, dps=dps)[0])
    
"""
3.77, 3, 12
gl_cdf = 
[mpf('0.94981479644775390625'),
 mpf('0.94981563091278076171875'),
 mpf('0.949817188084125518798828125'),
 mpf('0.949817637912929058074951172'),
 mpf('0.949817638262175023555755615'),
 mpf('0.949817638240347150713205338'),
 mpf('0.949817638240347150713205338'),
 mpf('0.949817638240006090200040489'),
 mpf('0.94981763823944476143879001'),
 mpf('0.94981763823944387326037031'),
 mpf('0.949817638239443651215765385'),
 mpf('0.94981763823944362346018977'),
 mpf('0.949817638239443475141332573'),
 mpf('0.949817638239443475249752791'),
 mpf('0.949817638239443475425935644'),
 mpf('0.949817638239443475430170808'),
 mpf('0.949817638239443475430064929'),
 mpf('0.949817638239443475398632066'),
 mpf('0.94981763823944347539862793'),
 mpf('0.94981763823944347539862762')]

ts_cdf = 
[mpf('0.949817657470703125'),
 mpf('0.949817657470703125'),
 mpf('0.94981764256954193115234375'),
 mpf('0.949817637912929058074951172'),
 mpf('0.949817637912929058074951172'),
 mpf('0.949817638123931828886270523'),
 mpf('0.949817638278545928187668324'),
 mpf('0.949817638239437656011432409'),
 mpf('0.94981763823944476143879001'),
 mpf('0.94981763823944298508195061'),
 mpf('0.94981763823944342917116046'),
 mpf('0.949817638239443470804523884'),
 mpf('0.949817638239443475141332573'),
 mpf('0.949817638239443475358173008'),
 mpf('0.949817638239443475398830589'),
 mpf('0.949817638239443475398830589'),
 mpf('0.949817638239443475398618831'),
 mpf('0.949817638239443475398632066'),
 mpf('0.949817638239443475398628757'),
 mpf('0.949817638239443475398628551')]

"""