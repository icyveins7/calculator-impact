#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 19:04:57 2021

@author: seolubuntu
"""

from PySide2.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PySide2.QtCore import Signal, Slot

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
        top.setMinimumWidth(160)
        
        separator = HLine()
        
        bottom = QLabel("Select %s to compare" % (typestring))
        bottom.setMinimumWidth(160)
        
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
        
        # Add Headers
        tbl1stat = QTableWidgetItem("Stat")
        tbl1val = QTableWidgetItem("Value")
        tbl2stat = QTableWidgetItem("Stat")
        tbl2val = QTableWidgetItem("Value")
        table1.setItem(0,0,tbl1stat)
        table1.setItem(0,1,tbl1val)
        table2.setItem(0,0,tbl2stat)
        table2.setItem(0,1,tbl2val)
        
        separator = HLine()
        
        self._widgetlayout.addWidget(vline)
        minilayout = QVBoxLayout()
        minilayout.addWidget(table1)
        minilayout.addWidget(separator)
        minilayout.addWidget(table2)
        self._widgetlayout.addLayout(minilayout)
        self._widgetlayout.addWidget(vline2)
        
        return table1, table2