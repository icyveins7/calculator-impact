# -*- coding: utf-8 -*-
"""
Created on Sat May 22 00:40:39 2021

@author: sandra
"""
from calcutils import check_stat
from workflow import read_image_to_artifact
from artifact_slots import *
import re

#%%separating stat names

results = read_image_to_artifact('4.png')

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
main_stat = main_label_dict[check_stat(results['mainstat']+results['mainstat_val'],mainstatstrs)]
substat1 = sub_label_dict[check_stat(results['substat1']+results['substat1_val'],substatstrs)]
substat2 = sub_label_dict[check_stat(results['substat2']+results['substat2_val'],substatstrs)]
substat3 = sub_label_dict[check_stat(results['substat3']+results['substat3_val'],substatstrs)]
substat4 = sub_label_dict[check_stat(results['substat4']+results['substat4_val'],substatstrs)]

#regex things
#1) change all Os in values to 0s


#arranging it into final dictionary and using fromDictionary to test

artifact_dict = {}
artifact_dict[main_stat]=results['mainstat_val']
artifact_dict[substat1]=results['substat1_val']
artifact_dict[substat2]=results['substat2_val']
artifact_dict[substat3]=results['substat3_val']
artifact_dict[substat4]=results['substat4_val']

print(artifact_dict)

# myartifact = Feather.fromDictionary(artifact_dict)
# myartifact.print()