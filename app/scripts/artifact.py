# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:39:27 2021

@author: Seo
"""

import numpy as np
import sqlite3 as sq

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
        self.typestr = "Artifact"
        
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
        

    def getAmalgamatedStats(self):
        mainstatkeys = ["mainhpraw",
                        "mainatkraw",
                        "mainhpperc",
                        "mainatkperc",
                        "maindefperc",
                        "mainer",
                        "mainem",
                        "maincritrate",
                        "maincritdmg",
                        "mainhealing",
                        "maincryo",
                        "mainanemo",
                        "maingeo",
                        "mainpyro",
                        "mainhydro",
                        "mainelec",
                        "mainphys"]
        substatkeys = ["atkraw",
                       "atkperc",
                       "hpraw",
                       "hpperc",
                       "critrate",
                       "critdmg",
                       "em",
                       "er",
                       "defraw",
                       "defperc"]
        
        # Extract non-None values
        validmainkeys = [key for key in mainstatkeys if getattr(self,key) is not None]
        validsubkeys = [key for key in substatkeys if getattr(self,key) is not None]
            
        # Output
        output = {}
        # main stat is a superset of substats, we key by the shorter substat key
        for key in validmainkeys:
            strippedmainkey = key[4:]
            if strippedmainkey in substatkeys: # for those mains that have an identical sub, use the sub as key
                output[strippedmainkey] = getattr(self, key)
            else: # otherwise for stuff like maincryo just use maincryo as the key
                output[key] = getattr(self,key)
            
        for key in validsubkeys:
            if key in output.keys(): # then just add to it (actually, this should never happen since no stat repeats)
                output[key] = output[key] + getattr(self, key)
            else: # otherwise create the key
                output[key] = getattr(self,key)
        
        return output
                
    def print(self):
        s = ""
        
        s = s + self.typestr + "\n----------\n"
        
        idx = [i for i, val in enumerate(self.mainstatlist) if val != None][0]
        # pretty printing based on if its % => move to end of string
        if self.mainstatstrs[idx][-1] == '%':
            self.mainstatstr = '%s +%.1f%%' % (self.mainstatstrs[idx][:-1], self.mainstatlist[idx])
        else:
            self.mainstatstr = '%s +%.1f' % (self.mainstatstrs[idx], self.mainstatlist[idx])
        # print(self.mainstatstr)
        s = s + self.mainstatstr + "\n----------\n"
        
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
            raise ValueError("Main stat must be HP%/ATK%/DEF%/CRIT Rate/CRIT DMG/Healing Bonus/Elemental Mastery.")
        
    @staticmethod
    def getMainStatKey(string=None):
        keydict = {"HP%": "mainhpperc",
                   "ATK%": "mainatkperc", 
                   "DEF%": "maindefperc", 
                   "CRIT Rate%": "maincritrate", 
                   "CRIT DMG%": "maincritdmg", 
                   "Healing Bonus%": "mainhealing",
                   "Elemental Mastery": "mainem"}
        if string is None:
            return keydict
        else:
            return keydict[string]
        
        
#%% 
class ArtifactDB:
    '''
    Note that the connection is not saved in this object.
    This is to ensure that the cursor will always be valid; otherwise, the
    cursor would be invalidated if the database was closed externally.
    '''
    def __init__(self, con, tablename='artifacts'):
        # Internal tablename
        self.tablename = tablename
        
        self.dictkeys = ["mainhpraw", "mainatkraw", "mainhpperc", "mainatkperc",
                    "maindefperc", "mainer", "mainem", "maincritrate",
                    "maincritdmg", "mainhealing", "maincryo",
                    "mainanemo", "maingeo", "mainpyro",
                    "mainhydro", "mainelec", "mainphys",
                    "atkraw", "atkperc", "hpraw", "hpperc",
                    "critrate", "critdmg", "em", "er",
                    "defraw", "defperc"] # this is in order, mainstats -> substats
        
        # Initialise table
        self.initTable(con)
        
        
    def initTable(self, con):
        cur = con.cursor()
        
        sql = "create table if not exists " + self.tablename + "(type int not null, "
        
        for key in self.dictkeys:
            sql = sql + key + " real, "
        
        sql = sql[:-2] # cut the last two chars off
        sql = sql + ")"
            
        try:
            cur.execute(sql)
        except sq.Error as e:
            print("Failed to initialize artifacts table!")
            raise(e)
            
    def clearTable(self, con):
        cur = con.cursor()
        
        sql = "delete from " + self.tablename

        try:
            cur.execute(sql)
            con.commit()
        except sq.Error as e:
            print("Failed to delete table contents!")
            raise(e)
            
    def deleteRows(self, ids, con):
        cur = con.cursor()
        
        qmarks = ("?," * len(ids))[:-1]
        sql = "delete from " + self.tablename + " where rowid in (%s)" % qmarks
        
        try:
            cur.execute(sql, ids)
            con.commit()
        except sq.Error as e:
            print("Failed to delete rows!")
            raise(e)
    
    def save(self, artifact, con):
        cur = con.cursor()
        
        sql = "insert into " + self.tablename + " values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        
        l = [artifact.type]
        l.extend(artifact.mainstatlist)
        l.extend(artifact.substatlist)

        try:
            cur.execute(sql, l)
            con.commit()
        except sq.Error as e:
            print("Failed to insert artifact into database!")
            raise(e)
            
    def load(self, con):
        con.row_factory = sq.Row
        cur = con.cursor()
        
        sql = "select rowid, * from " + self.tablename
        
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            artifacts, ids = self.rowsToArtifact(rows)
            
            return artifacts, ids
        except sq.Error as e:
            print("Failed to load artifacts!")
            raise(e)
            
    def rowsToArtifact(self, rows):
        artifacts = []
        ids = []
        for row in rows:
            d = dict(row) # convert
            atype = d.pop('type', None) # remove the type
            rowid = d.pop('rowid', None) # get the rowid
            ids.append(rowid)
            
            if atype == 1:
                artifacts.append(Flower.fromDictionary(d))
            elif atype == 2:
                artifacts.append(Feather.fromDictionary(d))
            elif atype == 3:
                artifacts.append(Timepiece.fromDictionary(d))
            elif atype == 4:
                artifacts.append(Goblet.fromDictionary(d))
            elif atype == 5:
                artifacts.append(Headpiece.fromDictionary(d))
                
        return artifacts, ids
        
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
        
    # DB tests
    con = sq.connect("test.db")
    artidb = ArtifactDB(con)
    
    flower = Flower(mainhpraw=100, atkperc=20)
    artidb.save(flower, con)
    
    feather = Feather(mainatkraw=200, atkperc=14)
    artidb.save(feather, con)
    
    tp = Timepiece(mainatkperc=12, defperc=14)
    artidb.save(tp, con)
    
    gob = Goblet(mainelec=22, defperc=11)
    artidb.save(gob, con)
    
    head = Headpiece(maincritrate=20, defperc=24)
    artidb.save(head, con)
    
    artifacts, ids = artidb.load(con)
    
    # check printing
    [i.print() for i in artifacts]
    print(ids)
    
    # delete some rows
    delids = [ids[0],ids[2],ids[4]]
    artidb.deleteRows(delids, con)
    
    # check again
    artifacts, ids = artidb.load(con)
    # check printing
    [i.print() for i in artifacts]
    print(ids)
    
    # clear all
    artidb.clearTable(con)
    
    con.close()
    