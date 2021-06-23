# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 00:05:42 2021

@author: Seo
"""

import skimage.io as skio
import os

cwd = os.path.dirname(os.path.abspath(__file__))
tessdata_dir = os.path.join(cwd,"..","tesseract_custom")
os.environ["TESSDATA_PREFIX"] = tessdata_dir
print("Set TESSDATA_PREFIX to %s" % (os.environ["TESSDATA_PREFIX"]))

import tessapi_wrapper

img = skio.imread("testimg.png")

print("Init-ing cython class")
try:
    citaw = tessapi_wrapper.PyCITessApiWrapper()
except:
    print("Failed to init cython class")
    
output = citaw.image_to_string("eng", img.tobytes(), img.shape[1], img.shape[0])
print(output)

output = citaw.image_to_string("gs", img.tobytes(), img.shape[1], img.shape[0])
print(output)

def citawtest(img, citaw):
    return citaw.image_to_string("eng", img.tobytes(), img.shape[1], img.shape[0])

print("Testing output by passing cython object into function")
output = citawtest(img, citaw)
print(output)

print("Testing whitelist")
whitelist = "0123456789.%"
output = citaw.image_to_string("eng", img.tobytes(), img.shape[1], img.shape[0], whitelist)
print(output)