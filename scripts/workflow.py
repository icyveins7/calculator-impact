# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:47:49 2021

@author: sandra
"""
from skimage import io
from skimage.color import rgb2gray
from calcutils import crop, check_mse, lock_button_init, crop_ref_lock, baby_image_proc,ocr_mainstat,ocr_substat
import os
import pytesseract
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

#%%identify lockbutton and referencepoint

image = io.imread(r'55.png')

gray_image = rgb2gray(image)

lockbutton1_prop,lockbutton2_prop = lock_button_init(lockbutton1,lockbutton2,gray_image)

lockbutton_ref = check_mse(lockbutton1_prop['error'],lockbutton2_prop['error'],lockbutton1_prop,lockbutton2_prop)
height,width = lockbutton_ref['data'].shape

import matplotlib.pyplot as plt

mainstat = crop_ref_lock(image,lockbutton_ref['y'],50,135,lockbutton_ref['x'],-400,-135)
mainstat_value = crop_ref_lock(image,lockbutton_ref['y'],50,135,lockbutton_ref['x'],-100,width+10)


#check if main stat has 2 lines, the substats are displaced
if '\n' in ocr_mainstat(mainstat).rstrip():
    level = crop_ref_lock(image,lockbutton_ref['y'],200,255,lockbutton_ref['x'],-390,-300)
    substat1 = crop_ref_lock(image,lockbutton_ref['y'],260,305,lockbutton_ref['x'],-363,width+10)
    substat2 = crop_ref_lock(image,lockbutton_ref['y'],305,350,lockbutton_ref['x'],-363,width+10)
    substat3 = crop_ref_lock(image,lockbutton_ref['y'],345,395,lockbutton_ref['x'],-363,width+10)
    substat4 = crop_ref_lock(image,lockbutton_ref['y'],395,440,lockbutton_ref['x'],-363,width+10)
else:
    level = crop_ref_lock(image,lockbutton_ref['y'],180,235,lockbutton_ref['x'],-390,-300)
    substat1 = crop_ref_lock(image,lockbutton_ref['y'],240,285,lockbutton_ref['x'],-363,width+10)
    substat2 = crop_ref_lock(image,lockbutton_ref['y'],285,330,lockbutton_ref['x'],-363,width+10)
    substat3 = crop_ref_lock(image,lockbutton_ref['y'],325,375,lockbutton_ref['x'],-363,width+10)
    substat4 = crop_ref_lock(image,lockbutton_ref['y'],375,420,lockbutton_ref['x'],-363,width+10)

plt.figure()
plt.imshow(mainstat)
plt.figure()
plt.imshow(mainstat_value)
plt.figure()
plt.imshow(level)
plt.figure()
plt.imshow(substat1)
plt.figure()
plt.imshow(substat2)
plt.figure()
plt.imshow(substat3)
plt.figure()
plt.imshow(substat4)


results = {'mainstat':ocr_mainstat(mainstat).rstrip().upper(),
                'mainstat_val':ocr_mainstat(mainstat_value).strip().upper(),
                'level':ocr_substat(level).strip().upper(),
                'substat1':ocr_substat(substat1).strip().upper(),
                'substat2':ocr_substat(substat2).strip().upper(),
                'substat3':ocr_substat(substat3).strip().upper(),
                'substat4':ocr_substat(substat4).strip().upper()
                }


transcribe = results['mainstat']+' '+results['mainstat_val']+'\n'+results['level']+'\n'+results['substat1']+'\n'+results['substat2']+'\n'+results['substat3']+'\n'+results['substat4']
print(transcribe)
