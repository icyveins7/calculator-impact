#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 23:29:40 2021

@author: seolubuntu
"""

from setuptools import setup, Extension

from Cython.Build import cythonize

extensions = [
    Extension("tessapi_wrapper", ["tessapi_wrapper.pyx"],
              libraries=["tesseract", "leptonica"],
              language = "c++")
    ]

setup(ext_modules=cythonize(extensions,
                            compiler_directives={'language_level' : 3}))