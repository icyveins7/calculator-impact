# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:17:52 2021

@author: Seo
"""

from artifact import Artifact
import numpy as np

#%%
class Flower(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Type
        self.type = 1
        self.typestr = "Flower"
        
        # Check the main stat is HP
        if self.mainhpraw is None:
            raise ValueError("Flower main stat must be HP.")
    
    @staticmethod
    def getMainStatKey(string=None):
        keydict = {"HP": "mainhpraw"}
        if string is None:
            return keydict
        else:
            return keydict[string]

#%%
class Feather(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Type
        self.type = 2
        self.typestr = "Feather"
        
        # Check the main stat is ATK
        if self.mainatkraw is None:
            raise ValueError("Feather main stat must be ATK.")
            
    @staticmethod
    def getMainStatKey(string=None):
        keydict = {"ATK": "mainatkraw"}
        if string is None:
            return keydict
        else:
            return keydict[string]
        
#%%
class Timepiece(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Type
        self.type = 3
        self.typestr = "Timepiece"
        
        # Check main stats allowed
        allowedMains = np.array([self.mainhpperc, self.mainatkperc, self.maindefperc,
                                 self.mainem, self.mainer])
        if np.all(allowedMains==None):
            raise ValueError("Main stat must be HP%/ATK%/DEF%/ER/EM.")
            
    @staticmethod
    def getMainStatKey(string=None):
        keydict = {"HP%": "mainhpperc",
                   "ATK%": "mainatkperc", 
                   "DEF%": "maindefperc", 
                   "Energy Recharge": "mainer", 
                   "Elemental Mastery": "mainem"}
        if string is None:
            return keydict
        else:
            return keydict[string]
        
                
#%%
class Goblet(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Type
        self.type = 4
        self.typestr = "Goblet"
        
        # Check main stats allowed
        allowedMains = np.array([self.mainhpperc, self.mainatkperc, self.maindefperc,
                                 self.mainem, self.maincryo, self.mainanemo, self.maingeo,
                                 self.mainpyro, self.mainhydro, self.mainelec, self.mainphys])
        if np.all(allowedMains==None):
            raise ValueError("Main stat must be HP%/ATK%/DEF%/EM/ELE DMG%/PHYS DMG%.")
            
    @staticmethod
    def getMainStatKey(string=None):
        keydict = {"HP%": "mainhpperc",
                   "ATK%": "mainatkperc", 
                   "DEF%": "maindefperc", 
                   "Elemental Mastery": "mainem",
                   "Cryo DMG Bonus%": "maincryo", 
                   "Anemo DMG Bonus%": "mainanemo", 
                   "Geo DMG Bonus%": "maingeo", 
                   "Pyro DMG Bonus%": "mainpyro", 
                   "Hydro DMG Bonus%": "mainhydro", 
                   "Electro DMG Bonus%": "mainelec", 
                   "Physical DMG Bonus%": "mainphys"}
        if string is None:
            return keydict
        else:
            return keydict[string]
            
#%%
class Headpiece(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Type
        self.type = 5
        self.typestr = "Headpiece"
        
        # Check main stats allowed
        allowedMains = np.array([self.mainhpperc, self.mainatkperc, self.maindefperc,
                                 self.mainem, self.maincritrate, self.maincritdmg, self.mainhealing])
        if np.all(allowedMains==None):
            raise ValueError("Main stat must be HP%/ATK%/DEF%/CRIT Rate/CRIT DMG/Healing Bonus.")
        
    @staticmethod
    def getMainStatKey(string=None):
        keydict = {"HP%": "mainhpperc",
                   "ATK%": "mainatkperc", 
                   "DEF%": "maindefperc", 
                   "CRIT Rate%": "maincritrate", 
                   "CRIT DMG%": "maincritdmg", 
                   "Healing Bonus%": "mainhealing"}
        if string is None:
            return keydict
        else:
            return keydict[string]
        
#%% Unit test
if __name__ == "__main__":
    # Test direct ctor
    feather = Feather(mainatkraw=123, atkperc=20.0, critrate=20.0, critdmg=20.0, er=100)
    goblet = Goblet(maincryo=46.0, atkperc=20.0, critrate=10.0, critdmg=12.0, em=50)
    
    feather.print()
    goblet.print()
    
    # Test dictionary ctor
    d = {'maincritdmg': 25.0, 'atkperc': 11.0, 'critrate': 12.0, 'em': 13, 'atkraw': 10}
    head = Headpiece.fromDictionary(d)
    head.print()
    
    # Test failures
    try:
        invalidflower = Flower(mainatkraw=10)
    except Exception as e:
        print(e)   
        
    try:
        invalidfeather = Feather(maincryo=10.0)
    except Exception as e:
        print(e)
        
    try:
        invalidTimepiece = Timepiece(mainer=10.0, mainem=10)
    except Exception as e:
        print(e)   
        
    try:
        invalidTimepiece = Timepiece(maincritdmg=10.0)
    except Exception as e:
        print(e)   
        
    try:
        invalidGoblet = Goblet(mainhealing=10.0)
    except Exception as e:
        print(e)  
        
    try:
        invalidHead = Headpiece(maincryo=10.0)
    except Exception as e:
        print(e) 