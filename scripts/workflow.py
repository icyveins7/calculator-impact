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
from skimage.feature import match_template


from cropping import crop, mse, check_lock_button
import os
import pytesseract
import matplotlib.pyplot as plt
import numpy as np


#%%
lockbutton1=rgb2gray(io.imread('lockbutton.png'))
lockbutton2=rgb2gray(io.imread('lockbutton2.png'))

#%% creating ss and cutting

os.chdir(r'imgs//ss')
dir_imgs = [i for i in os.listdir() if i.endswith(".png")==True ]

save_folder = 'saves'
os.mkdir(save_folder)

for img in dir_imgs:
    crop(save_folder,img,0.75,0.15,0.57)

#%% go into dir

os.chdir(save_folder)

#%%identify main and substats and save in folders for each figure

image = rgb2gray(io.imread(r'10.png'))

m1,x1,y1=check_lock_button(lockbutton1,image)
m2,x2,y2=check_lock_button(lockbutton2,image)

lockbutton1_prop = {'error':m1,'x':x1,'y':y1,'data':lockbutton1}
lockbutton2_prop = {'error':m2,'x':x2,'y':y2,'data':lockbutton2}

def check(m1,m2):
    if m1 < m2:
        lockbutton_ref = lockbutton1_prop
    else:
        lockbutton_ref = lockbutton2_prop
    return lockbutton_ref

lockbutton_ref = check(m1,m2)
height,width = lockbutton_ref['data'].shape
template = image[lockbutton_ref['y']:lockbutton_ref['y']+height,lockbutton_ref['x']:lockbutton_ref['x']+width]
mainstat = image[lockbutton_ref['y']+50:lockbutton_ref['y']+110,lockbutton_ref['x']-400:lockbutton_ref['x']+width+10]

plt.imshow(mainstat,plt.cm.gray)


#%%image processing
grayscale = mainstat

thresh = filters.threshold_sauvola(grayscale,window_size=53)
binary = grayscale < thresh

selem = morphology.disk(1)
res = morphology.black_tophat(binary,selem)

post_tophat = binary ^ res

plt.imshow((post_tophat),plt.cm.gray)

#%%
final_image = Image.fromarray((mainstat).astype('uint8'))
custom_config = r'--oem 0 --psm 6 -l gs'
result = pytesseract.image_to_string(final_image,config=custom_config)
print(result.strip())

plt.imshow(mainstat,plt.cm.gray)

#type, main, substats