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

warnings.simplefilter(action='ignore', category=FutureWarning)

image = imread(os.getcwd()+r'\imgs\ss\63.png')

myartifact = generate_dict(image)

artifact = Timepiece(**myartifact)
artifact.print()