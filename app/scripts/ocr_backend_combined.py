# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 00:36:35 2021

@author: Seo
"""

from PIL import Image
import numpy as np
from skimage.feature import match_template
import pytesseract
from skimage.color import rgb2gray

# from calcutils import cropping
# from workflow import read_image_to_artifact
import re
from difflib import SequenceMatcher

from skimage import io
from skimage.color import rgb2gray
# from calcutils import check_mse, lock_button_init, crop_ref_lock, ocr_mainstat,ocr_substat,ocr_values,split_substats
import os
import matplotlib.pyplot as plt


def cropping(im, height=1080, width=1920):
    # height, width, channels = im.shape # using input args
    
    ratio_left = 0.75
    ratio_top = 0.15
    ratio_bottom = 0.55
    
    x1 = int(ratio_left*width)
    x2 = width
    y1 = int(ratio_top*height)
    y2 = int(ratio_bottom*height)
    
    im1 = im[y1:y2,x1:x2,:]
    return im1

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

def lock_button_init(lockbutton1,lockbutton2,image):
    m1,x1,y1=check_lock_button(lockbutton1,image)
    m2,x2,y2=check_lock_button(lockbutton2,image)

    lockbutton1_prop = {'error':m1,'x':x1,'y':y1,'data':lockbutton1}
    lockbutton2_prop = {'error':m2,'x':x2,'y':y2,'data':lockbutton2}
    
    return(lockbutton1_prop,lockbutton2_prop)


def check_mse(m1,m2,lockbutton1_prop,lockbutton2_prop):
    if m1 < m2:
        lockbutton_ref = lockbutton1_prop
    else:
        lockbutton_ref = lockbutton2_prop
    return lockbutton_ref

def crop_ref_lock(image,y,add_y1,add_y2,x,add_x1,add_x2):
    cropped = image[y+add_y1:y+add_y2,x+add_x1:x+add_x2]
    return cropped

def baby_image_proc(image_array):
    im = Image.fromarray(image_array)
    source = im.split()

    R, G, B = 0, 1, 2

    # select regions where each colour is less than X
    threshold = 240
    for rgb in range(3):
        blackmask = source[rgb].point(lambda i: i < threshold and 255)
    
        # process the band to be black
        out = source[rgb].point(lambda i: i * 0)
    
        # paste the processed band back, but only where colour was < X
        source[rgb].paste(out, None, blackmask)
    
    newim = Image.merge(im.mode, source)
    return newim

def ocr_mainstat(img, citaw=None):
    img = baby_image_proc(img)
    if citaw is None: # use pytesseract
        custom_config = r'--oem 0 -l eng'
        result = pytesseract.image_to_string(img,config=custom_config)
        return result
    else: # use the new api reference
        width, height = img.size    
        img = np.fromstring(img.tobytes(), dtype=np.uint8)
        
        result = citaw.image_to_string("eng", img.tobytes(), width, height)
        return result.decode('utf-8')
    

def ocr_substat(img, citaw=None):
    if citaw is None:
        custom_config = r'--oem 0 --psm 13 -l gs -c tessedit_char_whitelist=abcdefghiklmnoprstuyABCDEFGHIKLMNOPRSTUY'   #removed j,q,v,w,x,z
        result = pytesseract.image_to_string(img,config=custom_config)
        return result
    else:
        whitelist = "abcdefghiklmnoprstuyABCDEFGHIKLMNOPRSTUY"
        result = citaw.image_to_string("gs", img.tobytes(), img.shape[1], img.shape[0], whitelist, psm=13)  #can edit this according to the custom config above?
        return result.decode('utf-8')
    

def ocr_values(img, citaw=None):
    if citaw is None:
        custom_config = r'--oem 0 --psm 13 -l gs -c tessedit_char_whitelist=0123456789.%'
        result = pytesseract.image_to_string(img,config=custom_config)
        return result
    else:
        whitelist = "0123456789.%"
        result = citaw.image_to_string("gs", img.tobytes(), img.shape[1], img.shape[0], whitelist, psm=13)   #can edit this according to the custom config above?
        return result.decode('utf-8')
    

def split_substats(substat,plusbutton):
    m_substat,x_substat,y_substat = check_lock_button(plusbutton,rgb2gray(substat))
    substat_label = crop_ref_lock(substat,y_substat,-y_substat,45,x_substat,-x_substat,0)
    substat_value = crop_ref_lock(substat,y_substat,-y_substat,45,x_substat,plusbutton.shape[1],substat.shape[1]-x_substat)
    return(substat_label,substat_value)


#%%
def read_image_to_artifact(ss_height,ss_width,height,width,image,citaw=None):
    gray_image = rgb2gray(image)
    key = str(ss_height)+'_'+str(ss_width)
    path= os.path.join("scripts","templates",key)
    
    lockbutton1=rgb2gray(io.imread(os.path.join(path,'lockbutton.png')))
    lockbutton2=rgb2gray(io.imread(os.path.join(path,'lockbutton2.png')))
    plusbutton = rgb2gray(io.imread(os.path.join(path,'plus_button.png')))

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
    
    
    #set values for cropping to be referred to for various reasons. can comment out when done
        
    mainstat_cropping = {'y1add':int(height/11.52),'y2add':int(height/4.27),'x1add':int(width/-1.6),'x2add':int(width/-4.7)}
    mainstat_val_cropping = {'y1add':int(height/11.52),'y2add':int(height/4.27),'x1add':int(width/-6.4),'x2add':width_lock+10}
    
    level_cropping_1 = {'y1add':int(height/3.2),'y2add':int(height/2.451),'x1add':int(width/-1.76),'x2add':int(width/-2.13)}
    substat1_cropping_1 = {'y1add':int(height/2.6),'y2add':int(height/2.021),'x1add':int(width/-1.76),'x2add':width_lock+10}
    substat2_cropping_1 = {'y1add':int(height/2.021),'y2add':int(height/1.745),'x1add':int(width/-1.76),'x2add':width_lock+10}
    substat3_cropping_1 = {'y1add':int(height/1.772),'y2add':int(height/1.536),'x1add':int(width/-1.76),'x2add':width_lock+10}
    substat4_cropping_1 = {'y1add':int(height/1.536),'y2add':int(height/1.371),'x1add':int(width/-1.76),'x2add':width_lock+10}

    level_cropping_2 = {'y1add':int(height/2.88),'y2add':int(height/2.26),'x1add':int(width/-1.76),'x2add':int(width/-2.13)}
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
        level = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.88),int(height/2.26),lockbutton_ref['x'],int(width/-1.76),int(width/-2.13))
        substat1 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.215),int(height/1.888),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat2 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.888),int(height/1.646),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat3 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.67),int(height/1.46),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat4 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.458),int(height/1.309),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        
        #for testing
        ax = plot_bounding(level_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+level_cropping_2['y1add'],\
                         level_cropping_2['y2add']-level_cropping_2['y1add'],level_cropping_2['x2add']-level_cropping_2['x1add'])
        
        ax = plot_bounding(substat1_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat1_cropping_2['y1add'],\
                         substat1_cropping_2['y2add']-substat1_cropping_2['y1add'],substat1_cropping_2['x2add']-substat1_cropping_2['x1add'])
        
        ax = plot_bounding(substat2_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat2_cropping_2['y1add'],\
                         substat2_cropping_2['y2add']-substat2_cropping_2['y1add'],substat2_cropping_2['x2add']-substat2_cropping_2['x1add'])
        
        ax = plot_bounding(substat3_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat3_cropping_2['y1add'],\
                         substat3_cropping_2['y2add']-substat3_cropping_2['y1add'],substat3_cropping_2['x2add']-substat3_cropping_2['x1add'])
        
        ax = plot_bounding(substat4_cropping_2['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+substat4_cropping_2['y1add'],\
                         substat4_cropping_2['y2add']-substat4_cropping_2['y1add'],substat4_cropping_2['x2add']-substat4_cropping_2['x1add'])    
        
    else:
        level = crop_ref_lock(image,lockbutton_ref['y'],int(height/3.2),int(height/2.451),lockbutton_ref['x'],int(width/-1.76),int(width/-2.13))
        substat1 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.6),int(height/2.021),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat2 = crop_ref_lock(image,lockbutton_ref['y'],int(height/2.021),int(height/1.745),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat3 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.772),int(height/1.536),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        substat4 = crop_ref_lock(image,lockbutton_ref['y'],int(height/1.536),int(height/1.371),lockbutton_ref['x'],int(width/-1.76),width_lock+10)
        
        #for testing
        ax = plot_bounding(level_cropping_1['x1add']+lockbutton_ref['x'],lockbutton_ref['y']+level_cropping_1['y1add'],\
                         level_cropping_1['y2add']-level_cropping_1['y1add'],level_cropping_1['x2add']-level_cropping_1['x1add'])
        
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
                    'level':ocr_values(level, citaw).strip().upper(),
                    'substat1':ocr_substat(substat1_label, citaw).strip().upper(),
                    'substat1_val':ocr_values(substat1_value, citaw).strip().upper(),
                    'substat2':ocr_substat(substat2_label, citaw).strip().upper(),
                    'substat2_val':ocr_values(substat2_value, citaw).strip().upper(),
                    'substat3':ocr_substat(substat3_label, citaw).strip().upper(),
                    'substat3_val':ocr_values(substat3_value, citaw).strip().upper(),
                    'substat4':ocr_substat(substat4_label, citaw).strip().upper(),
                    'substat4_val':ocr_values(substat4_value, citaw).strip().upper(),
                    }

    return(results,ax)


#%%
def similar(a, b):
    return SequenceMatcher(lambda x: x==" ", a, b).ratio()

def check_stat(stat,val_stat,strlist):
    values = []
    for i in strlist:
        values.append(similar(stat,i.upper()))
    
    max_val = max(values)
    index = values.index(max_val)
    label = strlist[index]
    if label in ['HP','ATK','DEF']:
        if '%' in val_stat:
            label = label+'%'
    
    return (max_val, label)

mainstatstrs = ['HP', 'ATK', #'HP%', 'ATK%',\
            'DEF%', 'Energy Recharge', 'Elemental Mastery', 'CRIT Rate%',\
            'CRIT DMG%', 'Healing Bonus%', 'Cryo DMG Bonus%',\
            'Anemo DMG Bonus%', 'Geo DMG Bonus%', 'Pyro DMG Bonus%',\
            'Hydro DMG Bonus%', 'Electro DMG Bonus%', 'Physical DMG Bonus%']   #remove HP%, DEF% and ATK%. They will be hardcoded
    

substatstrs = ['HP', 'ATK', #'HP%', 'ATK%',\
            'DEF',#'DEF%',\
            'Energy Recharge', 'Elemental Mastery', 'CRIT Rate%',\
            'CRIT DMG%']   #remove HP%, DEF% and ATK%. They will be hardcoded
    
main_label_dict={'HP':'mainhpraw', 'ATK':'mainatkraw', 'HP%':'mainhpperc', 'ATK%':'mainatkperc',\
            'DEF%':'maindefperc', 'Energy Recharge':'mainer', 'Elemental Mastery':'mainem', 'CRIT Rate%':'maincritrate',\
            'CRIT DMG%':'maincritdmg', 'Healing Bonus%':'mainhealing', 'Cryo DMG Bonus%':'maincryo',\
            'Anemo DMG Bonus%':'mainanemo', 'Geo DMG Bonus%':'maingeo', 'Pyro DMG Bonus%':'mainpyro',\
            'Hydro DMG Bonus%':'mainhydro', 'Electro DMG Bonus%':'mainelec', 'Physical DMG Bonus%':'mainphys'}
    
sub_label_dict={'HP':'hpraw', 'ATK':'atkraw', 'HP%':'hpperc', 'ATK%':'atkperc','DEF':'defraw',\
            'DEF%':'defperc', 'Energy Recharge':'er', 'Elemental Mastery':'em', 'CRIT Rate%':'critrate',\
            'CRIT DMG%':'critdmg'}

def generate_dict(ss_image, height=1080, width=1920, citaw=None):
    image = cropping(ss_image, height, width)
    # height = ss_image.shape[0]
    # width = ss_image.shape[1]
    results,ax = read_image_to_artifact(height,width,image.shape[0],image.shape[1],image,citaw)

    #check and save labels
    main_ratios,main_stat = check_stat(results['mainstat'],results['mainstat_val'],mainstatstrs)
    main_stat = main_label_dict[main_stat]
    substat1_ratios,substat1 = check_stat(results['substat1'],results['substat1_val'],substatstrs)
    substat2_ratios,substat2 = check_stat(results['substat2'],results['substat2_val'],substatstrs)
    substat3_ratios,substat3 = check_stat(results['substat3'],results['substat3_val'],substatstrs)
    substat4_ratios,substat4 = check_stat(results['substat4'],results['substat4_val'],substatstrs)
    
    #arranging it into final dictionary and using fromDictionary to test
    #filter out those substat which are too different from any substat
    
    artifact_dict = {}
    
    ratios_include = {'substat1':substat1_ratios,'substat2':substat2_ratios,'substat3':substat3_ratios,'substat4':substat4_ratios}
    print('\nRatios after similarity matching')
    print(ratios_include)
    substats_include = {'substat1':substat1,'substat2':substat2,'substat3':substat3,'substat4':substat4}
    values_include = {'substat1':results['substat1_val'],'substat2':results['substat2_val'],'substat3':results['substat3_val'],'substat4':results['substat4_val']}
    substats_to_include =[]
    
    for i in ratios_include.keys():
        check_mean = ratios_include[i]
        if check_mean >= 0.7049:
            substats_to_include.append(i)
    
    artifact_dict[main_stat]=results['mainstat_val']
    
    for stat in substats_to_include:
        artifact_dict[sub_label_dict[substats_include[stat]]]=values_include[stat]
    
    #do regex here after filtering all the values
    
    values_ = list(artifact_dict.values())
    stats_ = list(artifact_dict.keys())
    
    i = 0
    while i < len(values_):
        string = values_[i]
        
        #replace all : to .
        if ':' in string:
            string = string.replace(':','.')
        
        #if '..' is found, replace with only 1
        if '..' in string:
            string = string.replace('..','.')
        
        #detect more than 1 dot which can screw up regex
        if string.count('.')>1:
            string = string.split('.')[0]+'.'+string.split('.')[1]
        
        # #replace all O to 0
        # if 'O' in  string:
        #     string = string.replace('O','0')
        
        #remove all letters and other characters that shouldnt be there
        string = string.upper()
        string = re.sub('[^\d.]', "", string)
        
        #if stat is raw, need to remove all dots
        if 'raw' in  stats_[i]:
            string = string.replace('.','')
        
        z = re.findall(r'\d+[.]*\d*',string)
        
        #in case the filtering lets in letters and then after the regex there is nothing to find
        
        if len(z) == 0:
            z = 0
        else:
            z = float(z[0])
        
        #print(string,z)
        
        artifact_dict[stats_[i]]=z
        i+=1
        
    print('\nAfter regex and filtering by similarity matching')
    print(artifact_dict)
        
    return (results,artifact_dict,ax,image)