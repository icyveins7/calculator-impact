#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:04:57 2021

@author: seolubuntu
"""

from PySide2.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from PySide2.QtCore import Signal, SLOT

class ComparisonFrame(QFrame):
    def __init__(self):
        super().__init__()
        
        self._widgetlayout = QHBoxLayout()
        self.setLayout(self._widgetlayout)
        
        # Format the layout
        self.flower1, self.flower2 = self.addColumn("Flower",True)
        self.feather1, self.feather2 = self.addColumn("Feather",True)
        self.timepiece1, self.timepiece2 = self.addColumn("Timepiece",True)
        self.goblet1, self.goblet2 = self.addColumn("Goblet",True)
        self.headpiece1, self.headpiece2 = self.addColumn("Headpiece",True)
        
        self.summarytbl1, self.summarytbl2 = self.addSummaryTables()
        
    def addColumn(self, typestring, leftvline=False, rightvline=False):
        top = QLabel("Select %s to compare" % (typestring))
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        bottom = QLabel("Select %s to compare" % (typestring))
        
        minilayout = QVBoxLayout()
        minilayout.addWidget(top)
        minilayout.addWidget(separator)
        minilayout.addWidget(bottom)
        
        if leftvline:
            vline = QFrame()
            vline.setFrameShape(QFrame.VLine)
            vline.setFrameShadow(QFrame.Sunken)
            self._widgetlayout.addWidget(vline)
        
        self._widgetlayout.addLayout(minilayout)
        
        if rightvline:
            vline = QFrame()
            vline.setFrameShape(QFrame.VLine)
            vline.setFrameShadow(QFrame.Sunken)
            self._widgetlayout.addWidget(vline)
        
        return top, bottom
    
    def addSummaryTables(self):
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)
        vline2 = QFrame()
        vline2.setFrameShape(QFrame.VLine)
        vline2.setFrameShadow(QFrame.Sunken)
        
        table1 = QTableWidget(1,2)
        table2 = QTableWidget(1,2)
        
        # Add Headers
        tbl1stat = QTableWidgetItem("Stat")
        tbl1val = QTableWidgetItem("Value")
        tbl2stat = QTableWidgetItem("Stat")
        tbl2val = QTableWidgetItem("Value")
        table1.setItem(0,0,tbl1stat)
        table1.setItem(0,1,tbl1val)
        table2.setItem(0,0,tbl2stat)
        table2.setItem(0,1,tbl2val)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        self._widgetlayout.addWidget(vline)
        minilayout = QVBoxLayout()
        minilayout.addWidget(table1)
        minilayout.addWidget(separator)
        minilayout.addWidget(table2)
        self._widgetlayout.addLayout(minilayout)
        self._widgetlayout.addWidget(vline2)
        
        return table1, table2