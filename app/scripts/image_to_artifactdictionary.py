# -*- coding: utf-8 -*-
"""
Created on Sat May 29 15:25:10 2021

@author: sandra
"""

from string_filtering import generate_dict
import os
from artifact import *
import warnings
from skimage.io import imread
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)

# ss_image = imread(os.getcwd()+r'\imgs\ss\65.png')
ss_image = imread("F:/PycharmProjects/calculator-impact-labelled/image_2021-06-21_22-49-37.png")
# ss_image = imread("F:/PycharmProjects/calculator-impact-labelled/image_2021-06-21_22-52-56.png")
ss_image = imread("F:/PycharmProjects/calculator-impact-imgs/5_1080.png")
ss_image = ss_image[:,:,:3]

#1, 6 Flower
#2, 7 Feather
#3, 8 Timepiece
#4, 9 Goblet
#5, 0 Headpiece

results,myartifact,ax,image = generate_dict(ss_image, 1080, 1920)

print('\nAfter OCR')
print(results)
print('\n')
artifact = Goblet(**myartifact)
print('\nPrinting output on app:\n')
artifact.print()

ax.imshow(image)