# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:22:15 2021

@author: Seo
"""

from setuptools import setup, Extension

from Cython.Build import cythonize

extensions = [
    Extension("tessapi_wrapper", ["tessapi_wrapper.pyx"],
              include_dirs=["F:\\PycharmProjects\\vcpkg\\installed\\x64-windows\\include"],
              libraries=["tesseract41", "leptonica-1.80.0"],
              library_dirs=["F:\\PycharmProjects\\vcpkg\\installed\\x64-windows\\lib"],
              language = "c++")
    ]

setup(ext_modules=cythonize(extensions,
                            compiler_directives={'language_level' : 3}))