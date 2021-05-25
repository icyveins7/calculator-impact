# -*- coding: utf-8 -*-
"""
Created on Sat May 22 00:40:39 2021

@author: sandra
"""
from calcutils import check_stat
from workflow import read_image_to_artifact
from artifact_slots import *
import re
import numpy as np

#%%separating stat names

results = read_image_to_artifact('2.png')

mainstatstrs = ['HP', 'ATK', 'HP%', 'ATK%',\
            'DEF%', 'Energy Recharge', 'Elemental Mastery', 'CRIT Rate%',\
            'CRIT DMG%', 'Healing Bonus%', 'Cryo DMG Bonus%',\
            'Anemo DMG Bonus%', 'Geo DMG Bonus%', 'Pyro DMG Bonus%',\
            'Hydro DMG Bonus%', 'Electro DMG Bonus%', 'Physical DMG Bonus%']
    

substatstrs = ['HP', 'ATK', 'HP%', 'ATK%','DEF',\
            'DEF%', 'Energy Recharge', 'Elemental Mastery', 'CRIT Rate%',\
            'CRIT DMG%']
    
main_label_dict={'HP':'mainhpraw', 'ATK':'mainatkraw', 'HP%':'mainhpperc', 'ATK%':'mainatkperc',\
            'DEF%':'maindefperc', 'Energy Recharge':'mainer', 'Elemental Mastery':'mainem', 'CRIT Rate%':'maincritrate',\
            'CRIT DMG%':'maincritdmg', 'Healing Bonus%':'mainhealing', 'Cryo DMG Bonus%':'maincryo',\
            'Anemo DMG Bonus%':'mainanemo', 'Geo DMG Bonus%':'maingeo', 'Pyro DMG Bonus%':'mainpyro',\
            'Hydro DMG Bonus%':'mainhydro', 'Electro DMG Bonus%':'mainelec', 'Physical DMG Bonus%':'mainphys'}
    
sub_label_dict={'HP':'hpraw', 'ATK':'atkraw', 'HP%':'hpperc', 'ATK%':'atkperc','DEF':'defraw',\
            'DEF%':'defperc', 'Energy Recharge':'er', 'Elemental Mastery':'em', 'CRIT Rate%':'critrate',\
            'CRIT DMG%':'critdmg'}

#check and save labels
main_ratios,main_stat = check_stat(results['mainstat']+results['mainstat_val'],mainstatstrs)
main_stat = main_label_dict[main_stat]
substat1_ratios,substat1 = check_stat(results['substat1']+results['substat1_val'],substatstrs)
substat2_ratios,substat2 = check_stat(results['substat2']+results['substat2_val'],substatstrs)
substat3_ratios,substat3 = check_stat(results['substat3']+results['substat3_val'],substatstrs)
substat4_ratios,substat4 = check_stat(results['substat4']+results['substat4_val'],substatstrs)

#arranging it into final dictionary and using fromDictionary to test
#filter out those substat which are too different from any substat

artifact_dict = {}

ratios_include = {'substat1':substat1_ratios,'substat2':substat2_ratios,'substat3':substat3_ratios,'substat4':substat4_ratios}
substats_include = {'substat1':substat1,'substat2':substat2,'substat3':substat3,'substat4':substat4}
values_include = {'substat1':results['substat1_val'],'substat2':results['substat2_val'],'substat3':results['substat3_val'],'substat4':results['substat4_val']}
substats_to_include =[]

for i in ratios_include.keys():
    check_mean = ratios_include[i]
    if check_mean > 0.15:
        substats_to_include.append(i)

artifact_dict[main_stat]=results['mainstat_val']

for stat in substats_to_include:
    artifact_dict[sub_label_dict[substats_include[stat]]]=values_include[stat]

print(artifact_dict)

#do regex here after filtering all the values

# myartifact = Feather.fromDictionary(artifact_dict)
# myartifact.print()