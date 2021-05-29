# -*- coding: utf-8 -*-
"""
Created on Sat May 29 21:28:28 2021

@author: Seo
"""

import sqlite3 as sq
from artifact_slots import Flower, Feather, Timepiece, Goblet, Headpiece

class ArtifactDB:
    '''
    Note that the connection is not saved in this object.
    This is to ensure that the cursor will always be valid; otherwise, the
    cursor would be invalidated if the database was closed externally.
    '''
    def __init__(self, con, tablename='artifacts'):
        cur = con.cursor()
        
        self.dictkeys = ["mainhpraw", "mainatkraw", "mainhpperc", "mainatkperc",
                    "maindefperc", "mainer", "mainem", "maincritrate",
                    "maincritdmg", "mainhealing", "maincryo",
                    "mainanemo", "maingeo", "mainpyro",
                    "mainhydro", "mainelec", "mainphys",
                    "atkraw", "atkperc", "hpraw", "hpperc",
                    "critrate", "critdmg", "em", "er",
                    "defraw", "defperc"] # this is in order, mainstats -> substats
        
        sql = "create table if not exists " + tablename + "(type int not null, "
        
        for key in self.dictkeys:
            sql = sql + key + " real, "
        
        sql = sql[:-2] # cut the last two chars off
        sql = sql + ")"
            
        try:
            cur.execute(sql)
        except sq.Error as e:
            print("Failed to initialize artifacts table!")
            raise(e)
            
    def save(self, artifact, con, tablename='artifacts'):
        cur = con.cursor()
        
        sql = "insert into " + tablename + " values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        
        l = [artifact.type]
        l.extend(artifact.mainstatlist)
        l.extend(artifact.substatlist)

        try:
            cur.execute(sql, l)
            con.commit()
        except sq.Error as e:
            print("Failed to insert artifact into database!")
            raise(e)
            
    def load(self, con, tablename='artifacts'):
        con.row_factory = sq.Row
        cur = con.cursor()
        
        sql = "select * from " + tablename
        
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            artifacts = self.rowsToArtifact(rows)
            
            return artifacts
        except sq.Error as e:
            print("Failed to load artifacts!")
            raise(e)
            
    def rowsToArtifact(self, rows):
        artifacts = []
        for row in rows:
            d = dict(row) # convert
            atype = d.pop('type', None) # remove the type
            
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
                
        return artifacts
            
if __name__ == "__main__":
    con = sq.connect("test.db")
    artidb = ArtifactDB(con)
    
    flower = Flower(mainhpraw=100, atkperc=20)
    artidb.save(flower, con)
    
    feather = Feather(mainatkraw=200, atkperc=14)
    artidb.save(feather, con)
    
    artifacts = artidb.load(con)
    
    con.close()
    
    [i.print() for i in artifacts]
    