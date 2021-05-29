# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:47:49 2021

@author: sandra
"""
from skimage import io
from skimage.color import rgb2gray
from calcutils import check_mse, lock_button_init, crop_ref_lock, ocr_mainstat,ocr_substat,split_substats
import os

def read_image_to_artifact(image_filename):
    image = io.imread(image_filename)
    gray_image = rgb2gray(image)
    
    lockbutton1=rgb2gray(io.imread(os.getcwd()+'\lockbutton.png'))
    lockbutton2=rgb2gray(io.imread(os.getcwd()+'\lockbutton2.png'))
    plusbutton = rgb2gray(io.imread(os.getcwd()+'\plus_button.png'))

    lockbutton1_prop,lockbutton2_prop = lock_button_init(lockbutton1,lockbutton2,gray_image)

    lockbutton_ref = check_mse(lockbutton1_prop['error'],lockbutton2_prop['error'],lockbutton1_prop,lockbutton2_prop)
    height,width = lockbutton_ref['data'].shape

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
