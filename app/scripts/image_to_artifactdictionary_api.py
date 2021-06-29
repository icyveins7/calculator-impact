#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 00:07:34 2021

@author: seolubuntu
"""

from string_filtering import generate_dict
import sys
import os
from artifact import *
import warnings
from skimage.io import imread
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.getcwd(), "..","cpp"))
cwd = os.path.dirname(os.path.abspath(__file__))
tessdata_dir = os.path.join("..","..","tesseract_custom")
os.environ["TESSDATA_PREFIX"] = tessdata_dir
print("Set TESSDATA_PREFIX to %s" % (os.environ["TESSDATA_PREFIX"]))

import tessapi_wrapper

citaw = tessapi_wrapper.PyCITessApiWrapper()

warnings.simplefilter(action='ignore', category=FutureWarning)

ss_image = imread("F:/PycharmProjects/calculator-impact-imgs/5_1080.png")
ss_image = ss_image[:,:,:3]

#1, 6 Flower
#2, 7 Feather
#3, 8 Timepiece
#4, 9 Goblet
#5, 0 Headpiece

results,myartifact,ax,image = generate_dict(ss_image, 1080, 1920, citaw)

print(results)
print('\n')


# artifact = Flower(**myartifact)
# artifact.print()

ax.imshow(image)