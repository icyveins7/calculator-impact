# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:17:52 2021

@author: Seo
"""

from artifact import Artifact

#%%
class Flower(Artifact):
    def __init__(self, lv, mainhpraw,
                 atkraw=None, atkperc=None, hpperc=None,
                 critrate=None, critdmg=None, em=None, er=None,
                 defraw=None, defperc=None):
        
        super().__init__(lv=lv, mainhpraw=mainhpraw,
                         atkraw=atkraw, atkperc=atkperc,
                         hpperc=hpperc, critrate=critrate, critdmg=critdmg,
                         em=em, er=er, defraw=defraw, defperc=defperc)

#%%
class Feather(Artifact):
    def __init__(self, lv, mainatkraw,
                 atkperc=None, hpraw=None, hpperc=None,
                 critrate=None, critdmg=None, em=None, er=None,
                 defraw=None, defperc=None):
        
        super().__init__(lv=lv, mainatkraw=mainatkraw,
                         atkperc=atkperc, hpraw=hpraw,
                         hpperc=hpperc, critrate=critrate, critdmg=critdmg,
                         em=em, er=er, defraw=defraw, defperc=defperc)
        
#%%
class Timepiece(Artifact):
    def __init__(self, lv, mainhpperc=None, mainatkperc=None, maindefperc=None,
                 mainer=None, mainem=None,
                 atkraw=None, atkperc=None, hpraw=None, hpperc=None,
                 critrate=None, critdmg=None, em=None, er=None,
                 defraw=None, defperc=None):
        
        super().__init__(lv=lv, mainhpperc=mainhpperc, mainatkperc=mainatkperc, maindefperc=maindefperc,
                         mainer=mainer, mainem=mainem,
                         atkraw=atkraw, atkperc=atkperc, hpraw=hpraw,
                         hpperc=hpperc, critrate=critrate, critdmg=critdmg,
                         em=em, er=er, defraw=defraw, defperc=defperc)
        
#%%
class Goblet(Artifact):
    def __init__(self, lv, mainhpperc=None, mainatkperc=None, maindefperc=None,
                 mainem=None, maincryo=None, mainanemo=None, maingeo=None,
                 mainpyro=None, mainhydro=None, mainelec=None, mainphys=None,
                 atkraw=None, atkperc=None, hpraw=None, hpperc=None,
                 critrate=None, critdmg=None, em=None, er=None,
                 defraw=None, defperc=None):
        
        super().__init__(lv=lv, mainhpperc=mainhpperc, mainatkperc=mainatkperc, maindefperc=maindefperc,
                         mainem=mainem, maincryo=maincryo, mainanemo=mainanemo, maingeo=maingeo,
                         mainpyro=mainpyro, mainhydro=mainhydro, mainelec=mainelec, mainphys=mainphys,
                         atkraw=atkraw, atkperc=atkperc, hpraw=hpraw,
                         hpperc=hpperc, critrate=critrate, critdmg=critdmg,
                         em=em, er=er, defraw=defraw, defperc=defperc)
        
#%%
class Headpiece(Artifact):
    def __init__(self, lv, mainhpperc=None, mainatkperc=None, maindefperc=None,
                 mainem=None, maincritrate=None, maincritdmg=None, mainhealing=None,
                 atkraw=None, atkperc=None, hpraw=None, hpperc=None,
                 critrate=None, critdmg=None, em=None, er=None,
                 defraw=None, defperc=None):
        
        super().__init__(lv=lv, mainhpperc=mainhpperc, mainatkperc=mainatkperc, maindefperc=maindefperc,
                         mainem=mainem, maincritrate=maincritrate, maincritdmg=maincritdmg, mainhealing=mainhealing,
                         atkraw=atkraw, atkperc=atkperc, hpraw=hpraw,
                         hpperc=hpperc, critrate=critrate, critdmg=critdmg,
                         em=em, er=er, defraw=defraw, defperc=defperc)
        
#%% Unit test
if __name__ == "__main__":
    feather = Feather(20, 123, atkperc=20.0, critrate=20.0, critdmg=20.0, er=100)
    goblet = Goblet(20, maincryo=46.0, atkperc=20.0, critrate=10.0, critdmg=12.0, em=50)
    
    feather.print()
    goblet.print()