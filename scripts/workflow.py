# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:47:49 2021

@author: sandra
"""

from PIL import Image
import skimage
from skimage import filters, io
from skimage.color import rgb2gray
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage.exposure import rescale_intensity
from skimage.util import invert
from skimage.transform import resize
from skimage import morphology


from cropping import crop
import os
import pytesseract
import matplotlib.pyplot as plt
import numpy as np

#%% creating ss and cutting

os.chdir(r'imgs//ss')
dir_imgs = [i for i in os.listdir() if i.endswith(".png")==True ]

save_folder = 'saves'
os.mkdir(save_folder)

for img in dir_imgs:
    crop(save_folder,img)

#%% go into dir

os.chdir(save_folder)

#%%image processing

image = io.imread(r'48.png')

grayscale = rgb2gray(image)

thresh = filters.threshold_sauvola(grayscale,window_size=53)
binary = grayscale < thresh

selem = morphology.disk(1)
res = morphology.black_tophat(binary,selem)

post_tophat = binary ^ res

plt.imshow((post_tophat),plt.cm.gray)

final_image = Image.fromarray((binary).astype('uint8'))

custom_config = r'--oem 0 --psm 6 -l gs'
result = pytesseract.image_to_string(final_image,config=custom_config)
print(result.strip())

