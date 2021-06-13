#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 00:07:34 2021

@author: seolubuntu
"""

from string_filtering import generate_dict
import os
from artifact_slots import *
import warnings
from skimage.io import imread
import matplotlib.pyplot as plt
os.path.extend(os.path.join(os.getcwd(), "..","cpp"))
import tessapi_wrapper

citaw = tessapi_wrapper.PyCITessApiWrapper()

warnings.simplefilter(action='ignore', category=FutureWarning)

ss_image = imread(os.getcwd()+r'\imgs\ss\41.png')

#1, 6 Flower
#2, 7 Feather
#3, 8 Timepiece
#4, 9 Goblet
#5, 0 Headpiece

results,myartifact,ax,image = generate_dict(ss_image, citaw)

print(results)
print('\n')
artifact = Flower(**myartifact)
artifact.print()

ax.imshow(image)