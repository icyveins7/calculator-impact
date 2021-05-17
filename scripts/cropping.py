# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:43:45 2021

@author: sandra
"""

from PIL import Image
import os

def crop(directory,filename):
    im = Image.open(filename)
    width, height = im.size
    ratio_left = 0.75
    ratio_top = 0.15
    ratio_bottom = 0.55
    
    left = ratio_left*width
    right = width
    top = ratio_top*height
    bottom = height*ratio_bottom
    
    os.chdir(directory)
    
    im1 = im.crop((left,top,right,bottom))
    im1.save(filename)
    os.chdir('..')
    return 0