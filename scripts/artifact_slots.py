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
        
        # Check the main stat is HP
        if self.mainhpraw is None:
            raise ValueError("Flower main stat must be HP.")
        
    def print(self):
        print("Flower")
        super().print()

#%%
class Feather(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Check the main stat is ATK
        if self.mainatkraw is None:
            raise ValueError("Feather main stat must be ATK.")
        
    def print(self):
        print("Feather")
        super().print()
        
#%%
class Timepiece(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Check main stats allowed
        allowedMains = np.array([self.mainhpperc, self.mainatkperc, self.maindefperc,
                                 self.mainem, self.mainer])
        if np.all(allowedMains==None):
            raise ValueError("Main stat must be HP%/ATK%/DEF%/ER/EM.")
        
    
    def print(self):
        print("Timepiece")
        super().print()
        
#%%
class Goblet(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Check main stats allowed
        allowedMains = np.array([self.mainhpperc, self.mainatkperc, self.maindefperc,
                                 self.mainem, self.maincryo, self.mainanemo, self.maingeo,
                                 self.mainpyro, self.mainhydro, self.mainelec, self.mainphys])
        if np.all(allowedMains==None):
            raise ValueError("Main stat must be HP%/ATK%/DEF%/EM/ELE DMG%/PHYS DMG%.")
        
    def print(self):
        print("Goblet")
        super().print()
        
#%%
class Headpiece(Artifact):
    def __init__(self, **kwds):
        super().__init__(**kwds)
        
        # Check main stats allowed
        allowedMains = np.array([self.mainhpperc, self.mainatkperc, self.maindefperc,
                                 self.mainem, self.maincritrate, self.maincritdmg, self.mainhealing])
        if np.all(allowedMains==None):
            raise ValueError("Main stat must be HP%/ATK%/DEF%/CRIT Rate/CRIT DMG/Healing Bonus.")
        
        
    def print(self):
        print("Headpiece")
        super().print()
        
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