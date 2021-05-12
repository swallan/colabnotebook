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
    
with open("statsmodels_res_final.txt", "r") as f:
    sm = json.loads(f.readlines()[0])
    
with open("cython_res_final.txt", "r") as f:
    cython = json.loads(f.readlines()[0])
with open("r_res_final.txt", "r") as f:
    r = json.loads(f.readlines()[0])



gl_l = []
sm_l = []
c_l = []
r_l = []

for key in gl.keys():
    gl_l.append(mpf(gl[key]))
    sm_l.append(float(sm[key]))
    c_l.append(float(cython[key]))
    r_l.append(float(r[key]))
  
gl_l = np.asarray(gl_l)
sm_l = np.asarray(sm_l)
c_l = np.asarray(c_l)
r_l = np.asarray(r_l)

cython_errors = np.asarray(np.abs(c_l - gl_l), dtype=float)
sm_errors = np.asarray(np.abs(sm_l - gl_l), dtype=float)
r_errors = np.asarray(np.abs(r_l - gl_l), dtype=float)
#%%
import scipy.stats as stats
CI = .99
res_cython = stats.bootstrap((cython_errors,), np.mean, confidence_level=CI)
ci_cython = res_cython.confidence_interval
             
print(f"""             Mean Absolute Error CI\n
        Cython {CI*100}% Confidence Interval:
        ---------------------------------
             Lower     |     Upper
          -----------------------------
           {ci_cython.low:.3e}   |    {ci_cython.high:.3e}
      """)
      

res_sm = stats.bootstrap((sm_errors,), np.mean, confidence_level=CI)
ci_sm = res_sm.confidence_interval        
print(f"""\n\n
        Statsmodels {CI*100}% Confidence Interval:
        ---------------------------------
             Lower     |     Upper
          -----------------------------
           {ci_sm.low:.3e}   |    {ci_sm.high:.3e}
      """)    
     
# r results where v = 1 are NaN. filter them out.
r_errors_no_nans = r_errors[np.isfinite(r_errors)]    
     
res_r = stats.bootstrap((r_errors_no_nans,), np.mean, confidence_level=CI)
ci_r = res_r.confidence_interval        
print(f"""\n\n
            R {CI*100}%  Confidence Interval:
        ---------------------------------
             Lower     |     Upper
          -----------------------------
           {ci_r.low:.3e}  |    {ci_r.high:.3e}
      """)      
      
    #%%  
import scipy.stats as stats

pct = .99
threshold = 1e-12
sig_level = .01
res = stats.binomtest(cython_errors[cython_errors < threshold].shape[0], n=1000, p=pct,  alternative='greater')

print(f"""
Null hypothesis: We claim that at least {pct*100}% of results have are accurate, 
where accurate is defined by error less than {threshold}.
Out of 1000 results, {cython_errors[cython_errors < threshold].shape[0]} had errors less than than {threshold}.

Test this claim: 
>>> stats.binomtest({cython_errors[cython_errors < threshold].shape[0]}, n=1000, p={pct}, alternative='greater')
{res}

pvalue = {res.pvalue:.6f} {"<" if res.pvalue < sig_level else ">"} {sig_level}

Therefore, we do {"not " if res.pvalue < sig_level else ""}reject the null hypothesis. 
The observed values are {"" if res.pvalue < sig_level else "not "}within the range of the claim.

We can use the proportion_ci() method of the result to compute the confidence interval of the estimate:
>>> res.proportion_ci(confidence_level=.99)
{res.proportion_ci(confidence_level=.99)}
""")











