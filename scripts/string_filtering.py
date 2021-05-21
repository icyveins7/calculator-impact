# -*- coding: utf-8 -*-
"""
Created on Sat May 22 00:40:39 2021

@author: sandra
"""

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

results = {'mainstat':'ATK',
                'mainstat_val':'43%',
                'level':'+2O',
                'substat1':'ELEMENTALMASTERY+44',
                'substat2':'CRITRATE+7.4%',
                'substat3':'CRITDMG+7.O%',
                'substat4':'ENERGYRECHARGE+16.2%'
                }


mainstatstrs = ['HP', 'ATK', 'HP%', 'ATK%',\
            'DEF%', 'Energy Recharge', 'Elemental Mastery', 'CRIT Rate%',\
            'CRIT DMG%', 'Healing Bonus%', 'Cryo DMG Bonus%',\
            'Anemo DMG Bonus%', 'Geo DMG Bonus%', 'Pyro DMG Bonus%',\
            'Hydro DMG Bonus%', 'Electro DMG Bonus%', 'Physical DMG Bonus%']
    

substatstrs = ['HP', 'ATK', 'HP%', 'ATK%','DEF',\
            'DEF%', 'Energy Recharge', 'Elemental Mastery', 'CRIT Rate%',\
            'CRIT DMG%']
    

#check mainstat
values = []
for i in mainstatstrs:
    values.append(similar(results['mainstat']+results['mainstat_val'],i))
    
max_val = max(values)
index = values.index(max_val)
print(mainstatstrs[index])
