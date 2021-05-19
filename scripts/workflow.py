# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:47:49 2021

@author: sandra
"""
from skimage import io
from skimage.color import rgb2gray
from calcutils import crop, check_mse, lock_button_init, crop_ref_lock, baby_image_proc
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

image = io.imread(r'46.png')

gray_image = rgb2gray(image)

lockbutton1_prop,lockbutton2_prop = lock_button_init(lockbutton1,lockbutton2,gray_image)

lockbutton_ref = check_mse(lockbutton1_prop['error'],lockbutton2_prop['error'],lockbutton1_prop,lockbutton2_prop)
height,width = lockbutton_ref['data'].shape

mainstat = crop_ref_lock(image,lockbutton_ref['y'],50,135,lockbutton_ref['x'],-400,-135)
mainstat_value = crop_ref_lock(image,lockbutton_ref['y'],50,135,lockbutton_ref['x'],-100,width+10)

mainstat = baby_image_proc(mainstat)
mainstat_value = baby_image_proc(mainstat_value)

custom_config = r'--oem 0 -l eng'
main_stat_result = pytesseract.image_to_string(mainstat,config=custom_config)
main_stat_val_result = pytesseract.image_to_string(mainstat_value,config=custom_config)

result = main_stat_result.strip()+' '+main_stat_val_result.strip()
print(result)

#type, mainstat, substats, level, set