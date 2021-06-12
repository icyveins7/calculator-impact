# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 00:05:42 2021

@author: Seo
"""

import skimage.io as skio
import os
os.environ["TESSDATA_PREFIX"] = "F:\\PycharmProjects\\calculator-impact\\tesseract_custom"
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