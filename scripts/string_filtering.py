# -*- coding: utf-8 -*-
"""
Created on Sat May 22 00:40:39 2021

@author: sandra
"""

from calcutils import cropping
from workflow import read_image_to_artifact
import re
from difflib import SequenceMatcher

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
    image = cropping(ss_image)
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