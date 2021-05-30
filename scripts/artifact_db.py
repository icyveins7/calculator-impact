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
            artifacts = self.rowsToArtifact(rows)
            
            return artifacts
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
            
if __name__ == "__main__":
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
    
    
    