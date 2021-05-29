# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:47:49 2021

@author: sandra
"""
from skimage import io
from skimage.color import rgb2gray
from calcutils import check_mse, lock_button_init, crop_ref_lock, ocr_mainstat,ocr_substat,split_substats
import os

def read_image_to_artifact(height,width,image):
    gray_image = rgb2gray(image)

    lockbutton1=rgb2gray(io.imread(os.getcwd()+'\lockbutton.png'))
    lockbutton2=rgb2gray(io.imread(os.getcwd()+'\lockbutton2.png'))
    plusbutton = rgb2gray(io.imread(os.getcwd()+'\plus_button.png'))

    lockbutton1_prop,lockbutton2_prop = lock_button_init(lockbutton1,lockbutton2,gray_image)

    lockbutton_ref = check_mse(lockbutton1_prop['error'],lockbutton2_prop['error'],lockbutton1_prop,lockbutton2_prop)
    height_lock,width_lock = lockbutton_ref['data'].shape

    mainstat = crop_ref_lock(image,lockbutton_ref['y'],int(height/11.52),int(height/4.27),lockbutton_ref['x'],int(width/-1.6),int(width/-4.7))
    mainstat_value = crop_ref_lock(image,lockbutton_ref['y'],int(height/11.52),int(height/4.27),lockbutton_ref['x'],int(width/-6.4),width_lock+10)


    #check if main stat has 2 lines, the substats are displaced
    if '\n' in ocr_mainstat(mainstat).rstrip():
        level = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.88),int(height/2.26),lockbutton_ref['x'],int(width/-1.64),int(width/-2.13))
        substat1 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.215),int(height/1.888),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat2 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.888),int(height/1.646),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat3 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.67),int(height/1.46),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat4 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.458),int(height/1.309),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
    else:
        level = crop_ref_lock(image,lockbutton_ref['y'],int(height/3.2),int(height/2.451),lockbutton_ref['x'],int(width/-1.64),int(width/-2.13))
        substat1 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.6),int(height/2.021),lockbutton_ref['x'],-363,width_lock+10)
        substat2 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.021),int(height/1.745),lockbutton_ref['x'],-363,width_lock+10)
        substat3 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.772),int(height/1.536),lockbutton_ref['x'],-363,width_lock+10)
        substat4 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.536),int(height/1.371),lockbutton_ref['x'],-363,width_lock+10)    
    
    substat1_label,substat1_value = split_substats(substat1,plusbutton)
    substat2_label,substat2_value = split_substats(substat2,plusbutton)
    substat3_label,substat3_value = split_substats(substat3,plusbutton)
    substat4_label,substat4_value = split_substats(substat4,plusbutton)
    
    results = {'mainstat':ocr_mainstat(mainstat).rstrip().upper(),
                    'mainstat_val':ocr_mainstat(mainstat_value).strip().upper(),
                    'level':ocr_substat(level).strip().upper(),
                    'substat1':ocr_substat(substat1_label).strip().upper(),
                    'substat1_val':ocr_substat(substat1_value).strip().upper(),
                    'substat2':ocr_substat(substat2_label).strip().upper(),
                    'substat2_val':ocr_substat(substat2_value).strip().upper(),
                    'substat3':ocr_substat(substat3_label).strip().upper(),
                    'substat3_val':ocr_substat(substat3_value).strip().upper(),
                    'substat4':ocr_substat(substat4_label).strip().upper(),
                    'substat4_val':ocr_substat(substat4_value).strip().upper(),
                    }

    return(results)
