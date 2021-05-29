# -*- coding: utf-8 -*-
"""
Created on Sat May 29 15:25:10 2021

@author: sandra
"""

from string_filtering import generate_dict
import os
from artifact_slots import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

myartifact = generate_dict(os.getcwd()+r'\imgs\ss\saves\56.png')
artifact = Flower(**myartifact)
artifact.print()