#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:52:04 2021

@author: swallan
"""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()


lower, upper = -1.004e-12, 1.638e-12
ones = 1, 1
ax.plot((lower, upper), (1, 1), "ro-")
ax.plot(4.965513380714168e-13, 1, marker="|", markersize=20 )
ax.set_xlim(-1.004e-12*2, 1.638e-12*2)
ax.set_yticks([1])
ax.set_yticklabels(["cython"])
ax.set_title("99% Confidence Intervals Around Mean Absolute Error")
plt.figure(figsize=(10, 10))
# cc = np.abs(c)
# quant = np.quantile(cc, np.linspace(0, 1, 5))
# lin = np.linspace(cc.min(), cc.max(), 5)
# bins = (quant * .9 + lin * .1)
# ax.set_xscale('symlog', linthresh=1e-15)
# ax.hist(cc, bins='ft')

# ax.hist(cc * 10e10, bins=[0,.01, .05, .1, .2, .3, 1, 2, 3, 4, 5, 6, 7])
# ax.hist(c, bins=[0, 1e-15, 1e-14, 1e-13, 1e-12, 1e-11, 1e-10, 1e-09])
# 
# ax.plot(np.sort(c), np.arange(cc.shape[0]),)

# ax.set_xscale('symlog', linthresh=1e-24)
# ax.fill_betweenx([0, 1000], [lower, lower], [upper, upper], alpha=.4)
# plt.xlim(-1.638e-8, 1.638e-8)
plt.show()

#%%


# data_dict = {}
# data_dict['category'] = ['cython', "c1"]
# data_dict['lower'] = [-1.004e-12, -1.004e-12]
# data_dict['upper'] = [ 1.638e-12, 1.638e-12]
# for lower, upper, y in zip(data_dict['lower'], data_dict['upper'], range(len(data_dict))):
#     plt.plot((lower,upper),(y,y),'ro-',color='orange')
# plt.yticks(range(len(data_dict)),list(data_dict['category']))
# # plt.xlim(-1.004e-12*2, 1.638e-12*2)
# plt.show()