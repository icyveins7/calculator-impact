# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:47:49 2021

@author: sandra
"""
from skimage import io
from skimage.color import rgb2gray
from calcutils import check_mse, lock_button_init, crop_ref_lock, ocr_mainstat,ocr_substat,split_substats
import os
import matplotlib.pyplot as plt

def read_image_to_artifact(height,width,image,citaw=None):
    gray_image = rgb2gray(image)

    lockbutton1=rgb2gray(io.imread(os.getcwd()+'\\..\\scripts\\templates\\1080_1920\\lockbutton.png'))
    lockbutton2=rgb2gray(io.imread(os.getcwd()+'\\..\\scripts\\templates\\1080_1920\\lockbutton2.png'))
    plusbutton = rgb2gray(io.imread(os.getcwd()+'\\..\\scripts\\templates\\1080_1920\\plus_button.png'))

    lockbutton1_prop,lockbutton2_prop = lock_button_init(lockbutton1,lockbutton2,gray_image)

    lockbutton_ref = check_mse(lockbutton1_prop['error'],lockbutton2_prop['error'],lockbutton1_prop,lockbutton2_prop)
    height_lock,width_lock = lockbutton_ref['data'].shape
    
    #pre-define and save figure
    f = plt.figure(figsize=(6, 6))
    ax = plt.subplot()

    def plot_bounding(x,y,hcoin,wcoin,axis=ax,fig=f):
        rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
        axis.add_patch(rect)
        return(axis)
    
    ax = plot_bounding(lockbutton_ref['x'],lockbutton_ref['y'],height_lock,width_lock)
    
    
    #set values for cropping to be referred to for various reasons:
        
    mainstat_cropping = {'y1add':int(height/11.52),'y2add':int(height/4.27),'x1add':int(width/-1.6),'x2add':int(width/-4.7)}
    mainstat_val_cropping = {'y1add':int(height/11.52),'y2add':int(height/4.27),'x1add':int(width/-6.4),'x2add':width_lock+10}
    
    level_cropping_1 = {'y1add':int(height/3.2),'y2add':int(height/2.451),'x1add':int(width/-1.64),'x2add':int(width/-2.13)}
    substat1_cropping_1 = {'y1add':int(height/2.6),'y2add':int(height/2.021),'x1add':int(width/-1.76),'x2add':width_lock+10}
    substat2_cropping_1 = {'y1add':int(height/2.021),'y2add':int(height/1.745),'x1add':int(width/-1.76),'x2add':width_lock+10}
    substat3_cropping_1 = {'y1add':int(height/1.772),'y2add':int(height/1.536),'x1add':int(width/-1.76),'x2add':width_lock+10}
    substat4_cropping_1 = {'y1add':int(height/1.536),'y2add':int(height/1.371),'x1add':int(width/-1.76),'x2add':width_lock+10}

    level_cropping_2 = {'y1add':int(height/2.88),'y2add':int(height/2.26),'x1add':int(width/-1.64),'x2add':int(width/-2.13)}
    substat1_cropping_2 = {'y1add':int(height/2.215),'y2add':int(height/1.888),'x1add':int(width/-1.76),'x2add':width_lock+10}    
    substat2_cropping_2 = {'y1add':int(height/1.888),'y2add':int(height/1.646),'x1add':int(width/-1.76),'x2add':width_lock+10} 
    substat3_cropping_2 = {'y1add':int(height/1.67),'y2add':int(height/1.46),'x1add':int(width/-1.76),'x2add':width_lock+10}
    substat4_cropping_2 = {'y1add':int(height/1.458),'y2add':int(height/1.309),'x1add':int(width/-1.76),'x2add':width_lock+10}
    

    mainstat = crop_ref_lock(image,lockbutton_ref['y'],int(height/11.52),int(height/4.27),lockbutton_ref['x'],int(width/-1.6),int(width/-4.7))
    mainstat_value = crop_ref_lock(image,lockbutton_ref['y'],int(height/11.52),int(height/4.27),lockbutton_ref['x'],int(width/-6.4),width_lock+10)


    #add bounding boxes for testing
    ax = plot_bounding(mainstat_cropping['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+mainstat_cropping['y1add'],\
                         mainstat_cropping['y2add']-mainstat_cropping['y1add'],mainstat_cropping['x2add']-mainstat_cropping['x1add'])
        
    ax = plot_bounding(mainstat_val_cropping['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+mainstat_val_cropping['y1add'],\
                         mainstat_val_cropping['y2add']-mainstat_val_cropping['y1add'],mainstat_val_cropping['x2add']-mainstat_val_cropping['x1add'])


    #check if main stat has 2 lines, the substats are displaced
    if '\n' in ocr_mainstat(mainstat, citaw).rstrip():
        level = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.88),int(height/2.26),lockbutton_ref['x'],int(width/-1.64),int(width/-2.13))
        substat1 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.215),int(height/1.888),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat2 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.888),int(height/1.646),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat3 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.67),int(height/1.46),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat4 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.458),int(height/1.309),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        
        #for testing
        ax = plot_bounding(substat1_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat1_cropping_2['y1add'],\
                         substat1_cropping_2['y2add']-substat1_cropping_2['y1add'],substat1_cropping_2['x2add']-substat1_cropping_2['x1add'])
        
        ax = plot_bounding(substat2_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat2_cropping_2['y1add'],\
                         substat2_cropping_2['y2add']-substat2_cropping_2['y1add'],substat2_cropping_2['x2add']-substat2_cropping_2['x1add'])
        
        ax = plot_bounding(substat3_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat3_cropping_2['y1add'],\
                         substat3_cropping_2['y2add']-substat3_cropping_2['y1add'],substat3_cropping_2['x2add']-substat3_cropping_2['x1add'])
        
        ax = plot_bounding(substat4_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat4_cropping_2['y1add'],\
                         substat4_cropping_2['y2add']-substat4_cropping_2['y1add'],substat4_cropping_2['x2add']-substat4_cropping_2['x1add'])    
        
    else:
        level = crop_ref_lock(image,lockbutton_ref['y'],int(height/3.2),int(height/2.451),lockbutton_ref['x'],int(width/-1.64),int(width/-2.13))
        substat1 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.6),int(height/2.021),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat2 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.021),int(height/1.745),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat3 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.772),int(height/1.536),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat4 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.536),int(height/1.371),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        
        #for testing
        ax = plot_bounding(substat1_cropping_1['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat1_cropping_1['y1add'],\
                         substat1_cropping_1['y2add']-substat1_cropping_1['y1add'],substat1_cropping_1['x2add']-substat1_cropping_1['x1add'])
        
        ax = plot_bounding(substat2_cropping_1['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat2_cropping_1['y1add'],\
                         substat2_cropping_1['y2add']-substat2_cropping_1['y1add'],substat2_cropping_1['x2add']-substat2_cropping_1['x1add'])
        
        ax = plot_bounding(substat3_cropping_1['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat3_cropping_1['y1add'],\
                         substat3_cropping_1['y2add']-substat3_cropping_1['y1add'],substat3_cropping_1['x2add']-substat3_cropping_1['x1add'])
        
        ax = plot_bounding(substat4_cropping_1['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat4_cropping_1['y1add'],\
                         substat4_cropping_1['y2add']-substat4_cropping_1['y1add'],substat4_cropping_1['x2add']-substat4_cropping_1['x1add'])  
        
    
    substat1_label,substat1_value = split_substats(substat1,plusbutton)
    substat2_label,substat2_value = split_substats(substat2,plusbutton)
    substat3_label,substat3_value = split_substats(substat3,plusbutton)
    substat4_label,substat4_value = split_substats(substat4,plusbutton)
    
    results = {'mainstat':ocr_mainstat(mainstat,citaw).rstrip().upper(),
                    'mainstat_val':ocr_mainstat(mainstat_value, citaw).strip().upper(),
                    'level':ocr_substat(level, citaw).strip().upper(),
                    'substat1':ocr_substat(substat1_label, citaw).strip().upper(),
                    'substat1_val':ocr_substat(substat1_value, citaw).strip().upper(),
                    'substat2':ocr_substat(substat2_label, citaw).strip().upper(),
                    'substat2_val':ocr_substat(substat2_value, citaw).strip().upper(),
                    'substat3':ocr_substat(substat3_label, citaw).strip().upper(),
                    'substat3_val':ocr_substat(substat3_value, citaw).strip().upper(),
                    'substat4':ocr_substat(substat4_label, citaw).strip().upper(),
                    'substat4_val':ocr_substat(substat4_value, citaw).strip().upper(),
                    }

    return(results,ax)
