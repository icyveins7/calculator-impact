# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:43:45 2021

@author: sandra
"""

from PIL import Image
import os
import numpy as np
from skimage.feature import match_template


def crop(directory,filename,ratio_left,ratio_top,ratio_bottom):
    im = Image.open(filename)
    width, height = im.size
    
    left = ratio_left*width
    right = width
    top = ratio_top*height
    bottom = height*ratio_bottom
    
    os.chdir(directory)
    
    im1 = im.crop((left,top,right,bottom))
    im1.save(filename)
    os.chdir('..')
    return 0

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def check_lock_button(lockbutton,image):
    result = match_template(image,lockbutton)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[::-1]
    height, width = lockbutton.shape    
    identified_img = image[y:y+height,x:x+width]
    m = mse(lockbutton,identified_img)
    return m,x,y