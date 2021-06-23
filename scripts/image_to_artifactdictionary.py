# -*- coding: utf-8 -*-
"""
Created on Sat May 29 15:25:10 2021

@author: sandra
"""

from string_filtering import generate_dict
import os
from artifact_slots import *
import warnings
from skimage.io import imread
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)

ss_image = imread(os.getcwd()+r'\imgs\ss\65.png')

#1, 6 Flower
#2, 7 Feather
#3, 8 Timepiece
#4, 9 Goblet
#5, 0 Headpiece

results,myartifact,ax,image = generate_dict(ss_image)

print('\nAfter OCR')
print(results)
print('\n')
artifact = Headpiece(**myartifact)
print('\nPrinting output on app:\n')
artifact.print()

ax.imshow(image)