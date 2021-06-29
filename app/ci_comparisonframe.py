#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:04:57 2021

@author: seolubuntu
"""

from PySide2.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PySide2.QtCore import Signal, Slot

import sys
from scripts.artifact import *

class HLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        
class VLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
    
class ComparisonFrame(QFrame):
    insertRequestSignal = Signal(int)
    def __init__(self):
        super().__init__()
        
        self._widgetlayout = QHBoxLayout()
        self.setLayout(self._widgetlayout)
        
        # Format the layout
        self.add1btn, self.add2btn = self.addInsertButtons(True)
        
        self.flower1, self.flower2 = self.addColumn("Flower",True)
        self.feather1, self.feather2 = self.addColumn("Feather",True)
        self.timepiece1, self.timepiece2 = self.addColumn("Timepiece",True)
        self.goblet1, self.goblet2 = self.addColumn("Goblet",True)
        self.headpiece1, self.headpiece2 = self.addColumn("Headpiece",True)
        
        self.summarytbl1, self.summarytbl2 = self.addSummaryTables()
        self.resetTables() # reset and add headers
        
        # Dictionary for easy access
        self.displays = {0:[self.flower1, self.feather1, self.timepiece1, self.goblet1, self.headpiece1],
                         1:[self.flower2, self.feather2, self.timepiece2, self.goblet2, self.headpiece2]}
        self.artifactholders = {0:{1:None,2:None,3:None,4:None,5:None},
                                1:{1:None,2:None,3:None,4:None,5:None}}
        self.tables = [self.summarytbl1, self.summarytbl2]
        
        # Connections
        self.add1btn.clicked.connect(self.add1btnClicked)
        self.add2btn.clicked.connect(self.add2btnClicked)
        
    @Slot()
    def add1btnClicked(self):
        print("Request insert to top")
        self.insertRequestSignal.emit(0)
    
    @Slot()
    def add2btnClicked(self):
        print("Request insert to btm")
        self.insertRequestSignal.emit(1)
        
    @Slot(list, int)
    def insertArtifacts(self, artifactlist, idx):
        for atype in range(1,6):
            artifacts = [i for i in artifactlist if i.type==atype]
            if len(artifacts) > 1:
                raise TypeError("More than 1 %s selected." % (artifacts[0].typestr))
            elif len(artifacts) > 0:
                artifact = artifacts[0]
                self.displays[idx][atype-1].setText(artifact.print())
                # Set the artifact for this display for access by the table
                self.artifactholders[idx][atype] = artifact
                
        # Update the table
        self.updateTables()    
        
    @Slot()
    def updateTables(self):
        statdict = Artifact.getStatString()
        self.resetTables() # reset both tables
        
        for i in range(2): # top/btm
            valdicts = []
            for j in range(1,6): # iterate over slot
                if self.artifactholders[i][j] is not None:
                    valdicts.append(self.artifactholders[i][j].getAmalgamatedStats())
                    
            combinedvals = {}
            for d in valdicts:
                combinedvals = {k: combinedvals.get(k, 0) + d.get(k, 0) for k in set(combinedvals) | set(d)}
        
            print(combinedvals)
            # update the table
            self.tables[i].setRowCount(1 + len(combinedvals.keys()))
            row = 1
            for key, value in combinedvals.items():
                stringitem = QTableWidgetItem(statdict[key])
                valitem = QTableWidgetItem("%.1f" % (value))
                self.tables[i].setItem(row, 0, stringitem)
                self.tables[i].setItem(row, 1, valitem)
                row = row + 1
                
        
    
    def addInsertButtons(self, leftvline=False, rightvline=False):
        add1btn = QPushButton("=>")
        add2btn = QPushButton("=>")
        add1btn.setMaximumWidth(24)
        add2btn.setMaximumWidth(24)
        hline = HLine()
        vlayout = QVBoxLayout()
        vlayout.addWidget(add1btn)
        vlayout.addWidget(hline)
        vlayout.addWidget(add2btn)
        self._widgetlayout.addLayout(vlayout)
        
        return add1btn, add2btn
        
    def addColumn(self, typestring, leftvline=False, rightvline=False):
        top = QLabel("Select %s to compare" % (typestring))
        top.setMinimumWidth(144)
        
        separator = HLine()
        
        bottom = QLabel("Select %s to compare" % (typestring))
        bottom.setMinimumWidth(144)
        
        minilayout = QVBoxLayout()
        minilayout.addWidget(top)
        minilayout.addWidget(separator)
        minilayout.addWidget(bottom)
        
        if leftvline:
            vline = VLine()
            self._widgetlayout.addWidget(vline)
        
        self._widgetlayout.addLayout(minilayout)
        
        if rightvline:
            vline = VLine()
            self._widgetlayout.addWidget(vline)
        
        return top, bottom
    
    def addSummaryTables(self):
        vline = VLine()
        vline2 = VLine()
        
        table1 = QTableWidget(1,2)
        table2 = QTableWidget(1,2)
        table1.verticalHeader().setVisible(False)
        table1.horizontalHeader().setVisible(False)
        table2.verticalHeader().setVisible(False)
        table2.horizontalHeader().setVisible(False)
        
        # Column widths
        table1.setColumnWidth(0, 144)
        table1.setColumnWidth(1, 48)
        table2.setColumnWidth(0, 144)
        table2.setColumnWidth(1, 48)
        
        separator = HLine()
        
        self._widgetlayout.addWidget(vline)
        minilayout = QVBoxLayout()
        minilayout.addWidget(table1)
        minilayout.addWidget(separator)
        minilayout.addWidget(table2)
        self._widgetlayout.addLayout(minilayout)
        self._widgetlayout.addWidget(vline2)
        
        return table1, table2
    
    def resetTables(self):
        self.summarytbl1.clear()
        self.summarytbl2.clear()
        self.summarytbl1.setRowCount(1)
        self.summarytbl2.setRowCount(1)
        
        self.tbl1stat = QTableWidgetItem("Stat")
        self.tbl1val = QTableWidgetItem("Value")
        self.tbl2stat = QTableWidgetItem("Stat")
        self.tbl2val = QTableWidgetItem("Value")
        self.summarytbl1.setItem(0,0,self.tbl1stat)
        self.summarytbl1.setItem(0,1,self.tbl1val)
        self.summarytbl2.setItem(0,0,self.tbl2stat)
        self.summarytbl2.setItem(0,1,self.tbl2val)