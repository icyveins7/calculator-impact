# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:39:27 2021

@author: Seo
"""

class Artifact:
    def __init__(self,
                 mainhpraw=None, mainatkraw=None, mainhpperc=None, mainatkperc=None,
                 maindefperc=None, mainer=None, mainem=None,
                 maincritrate=None, maincritdmg=None, mainhealing=None,
                 maincryo=None, mainanemo=None, maingeo=None,
                 mainpyro=None, mainhydro=None, mainelec=None, mainphys=None,
                 atkraw=None, atkperc=None, hpraw=None, hpperc=None,
                 critrate=None, critdmg=None, em=None, er=None,
                 defraw=None, defperc=None):
        
        # Type identifiers (0 - 5, 0 being plain artifact, 1-5 being slot number)
        self.type = 0
        
        # Main stats which may clash
        self.mainhpraw = mainhpraw
        self.mainatkraw = mainatkraw
        self.mainhpperc = mainhpperc
        self.mainatkperc = mainatkperc
        self.maindefperc = maindefperc
        self.mainer = mainer
        self.mainem = mainem
        self.maincritrate = maincritrate
        self.maincritdmg = maincritdmg
        
        # Main stats which cannot clash
        self.mainhealing = mainhealing
        self.maincryo = maincryo
        self.mainanemo = mainanemo
        self.maingeo = maingeo
        self.mainpyro = mainpyro
        self.mainhydro = mainhydro
        self.mainelec = mainelec
        self.mainphys = mainphys
        
        # Sub stats
        self.atkraw = atkraw
        self.atkperc = atkperc
        self.hpraw = hpraw
        self.hpperc = hpperc
        self.critrate = critrate
        self.critdmg = critdmg
        self.em = em
        self.er = er
        self.defraw = defraw
        self.defperc = defperc
        
        # Check only up to 1 main stat
        self.mainstatlist = [self.mainhpraw, self.mainatkraw, self.mainhpperc, self.mainatkperc,
                        self.maindefperc, self.mainer, self.mainem, self.maincritrate,
                        self.maincritdmg, self.mainhealing, self.maincryo,
                        self.mainanemo, self.maingeo, self.mainpyro,
                        self.mainhydro, self.mainelec, self.mainphys]
        self.mainstatstrs = ['HP', 'ATK', 'HP%', 'ATK%',
                            'DEF%', 'Energy Recharge', 'Elemental Mastery', 'CRIT Rate%',
                            'CRIT DMG%', 'Healing Bonus%', 'Cryo DMG Bonus%',
                            'Anemo DMG Bonus%', 'Geo DMG Bonus%', 'Pyro DMG Bonus%',
                            'Hydro DMG Bonus%', 'Electro DMG Bonus%', 'Physical DMG Bonus%']
        if len(self.mainstatlist) - self.mainstatlist.count(None) > 1:
            raise ValueError("Cannot have more than 1 main stat.")
        elif self.mainstatlist.count(None) == len(self.mainstatlist):
            raise ValueError("Must have at least 1 main stat.")
        
    
        # Check only up to 4 substats
        self.substatlist = [self.atkraw, self.atkperc, self.hpraw, self.hpperc,
                       self.critrate, self.critdmg, self.em, self.er,
                       self.defraw, self.defperc]
        self.substatstrs = ['ATK', 'ATK%', 'HP', 'HP%', 'CRIT Rate%',
                            'CRIT DMG%', 'Elemental Mastery', 'Energy Recharge',
                            'DEF', 'DEF%']
        if len(self.substatlist) - self.substatlist.count(None) > 4:
            raise ValueError("Cannot have more than 4 substats.")

        # Check no substat-mainstat clashes
        if self.mainhpraw is not None and self.hpraw is not None:
            raise ValueError("Cannot have both main/sub stats as HP.")
        if self.mainatkraw is not None and self.atkraw is not None:
            raise ValueError("Cannot have both main/sub stats as ATK.")
        if self.mainhpperc is not None and self.hpperc is not None:
            raise ValueError("Cannot have both main/sub stats as HP%.")
        if self.mainatkperc is not None and self.atkperc is not None:
            raise ValueError("Cannot have both main/sub stats as ATK%.")
        if self.maindefperc is not None and self.defperc is not None:
            raise ValueError("Cannot have both main/sub stats as DEF%.")
        if self.mainer is not None and self.er is not None:
            raise ValueError("Cannot have both main/sub stats as Energy Recharge.")
        if self.mainem is not None and self.em is not None:
            raise ValueError("Cannot have both main/sub stats as Elemental Mastery.")
        if self.maincritrate is not None and self.critrate is not None:
            raise ValueError("Cannot have both main/sub stats as CRIT Rate%.")
        if self.maincritdmg is not None and self.critdmg is not None:
            raise ValueError("Cannot have both main/sub stats as CRIT DMG%.")

    @staticmethod
    def getStatString(mainstatkey=None):
        stringdict = {"mainhpraw": "HP",
                      "mainatkraw": "ATK",
                      "mainhpperc": "HP%",
                      "mainatkperc": "ATK%",
                      "maindefperc": "DEF%",
                      "mainer": "Energy Recharge",
                      "mainem": "Elemental Mastery",
                      "maincritrate": "CRIT Rate%",
                      "maincritdmg": "CRIT DMG%",
                      "mainhealing": "Healing Bonus%",
                      "maincryo": "Cryo DMG Bonus%",
                      "mainanemo": "Anemo DMG Bonus%",
                      "maingeo": "Geo DMG Bonus%",
                      "mainpyro": "Pyro DMG Bonus%",
                      "mainhydro": "Hydro DMG Bonus%",
                      "mainelec": "Electro DMG Bonus%",
                      "mainphys": "Physical DMG Bonus%",
                      "atkraw": "ATK",
                      "atkperc": "ATK%",
                      "hpraw": "HP",
                      "hpperc": "HP%",
                      "critrate": "CRIT Rate%",
                      "critdmg": "CRIT DMG%",
                      "em": "Elemental Mastery",
                      "er": "Energy Recharge",
                      "defraw": "DEF",
                      "defperc": "DEF%"}
        if mainstatkey is None:
            return stringdict
        else:
            return stringdict[mainstatkey]
    
    @staticmethod
    def getMainStatKey(string=None):
        keydict = {"HP": "mainhpraw",
                   "ATK": "mainatkraw",
                   "HP%": "mainhpperc",
                   "ATK%": "mainatkperc", 
                   "DEF%": "maindefperc", 
                   "Energy Recharge": "mainer", 
                   "Elemental Mastery": "mainem", 
                   "CRIT Rate%": "maincritrate", 
                   "CRIT DMG%": "maincritdmg", 
                   "Healing Bonus%": "mainhealing", 
                   "Cryo DMG Bonus%": "maincryo", 
                   "Anemo DMG Bonus%": "mainanemo", 
                   "Geo DMG Bonus%": "maingeo", 
                   "Pyro DMG Bonus%": "mainpyro", 
                   "Hydro DMG Bonus%": "mainhydro", 
                   "Electro DMG Bonus%": "mainelec", 
                   "Physical DMG Bonus%": "mainphys"}
        return keydict[string]
        
    @staticmethod
    def getSubStatKey(string):
        keydict = {"ATK": "atkraw", 
                   "ATK%": "atkperc", 
                   "HP": "hpraw", 
                   "HP%": "hpperc", 
                   "CRIT Rate%": "critrate", 
                   "CRIT DMG%": "critdmg", 
                   "Elemental Mastery": "em", 
                   "Energy Recharge": "er", 
                   "DEF": "defraw", 
                   "DEF%": "defperc"}
        return keydict[string]

    @classmethod
    def fromDictionary(cls, d):
        '''
        For more explicit unpacking of the dictionary.
        Of course, doing Artifact(**d) has the same effect.
        '''
        return cls(**d)
        

    def print(self):
        s = ""
        
        s = s + self.typestr + "\n"
        
        idx = [i for i, val in enumerate(self.mainstatlist) if val != None][0]
        # pretty printing based on if its % => move to end of string
        if self.mainstatstrs[idx][-1] == '%':
            self.mainstatstr = '(Main) %s +%.1f%%' % (self.mainstatstrs[idx][:-1], self.mainstatlist[idx])
        else:
            self.mainstatstr = '(Main) %s +%.1f' % (self.mainstatstrs[idx], self.mainstatlist[idx])
        # print(self.mainstatstr)
        s = s + self.mainstatstr + "\n"
        
        # substat printing
        if self.atkraw is not None:
            s = s + ("ATK+%d" % self.atkraw) + "\n"
            # print("ATK+%d" % self.atkraw)
        if self.atkperc is not None:
            s = s + ("ATK+%.1f%%" % self.atkperc) + "\n"
            # print("ATK+%.1f%%" % self.atkperc)
        if self.hpraw is not None:
            s = s + ("HP+%d" % self.hpraw) + "\n"
            # print("HP+%d" % self.hpraw)
        if self.hpperc is not None:
            s = s + ("HP+%.1f%%" % self.hpperc) + "\n"
            # print("HP+%.1f%%" % self.hpperc)
        if self.critrate is not None:
            s = s + ("CRIT Rate+%.1f%%" % self.critrate) + "\n"
            # print("CRIT Rate+%.1f%%" % self.critrate)
        if self.critdmg is not None:
            s = s + ("CRIT DMG+%.1f%%" % self.critdmg) + "\n"
            # print("CRIT DMG+%.1f%%" % self.critdmg)
        if self.em is not None:
            s = s + ("Elemental Mastery+%d" % self.em) + "\n"
            # print("Elemental Mastery+%d" % self.em)
        if self.er is not None:
            s = s + ("Energy Recharge+%.1f%%" % self.er) + "\n"
            # print("Energy Recharge+%.1f%%" % self.er)
        if self.defraw is not None:
            s = s + ("DEF+%d" % self.defraw) + "\n"
            # print("DEF+%d" % self.defraw)
        if self.defperc is not None:
            s = s + ("DEF+%.1f%%" % self.defperc) + "\n"
            # print("DEF+%.1f%%" % self.defperc)
            
        print(s)
        
        return s

        