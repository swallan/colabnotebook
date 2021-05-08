#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 18:16:34 2021

@author: swallan
"""

from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize('srd.pyx'))