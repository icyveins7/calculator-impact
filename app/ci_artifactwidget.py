# -*- coding: utf-8 -*-
"""
Created on Fri May 21 23:38:23 2021

@author: Seo
"""

# from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PySide2.QtWidgets import QPushButton, QLineEdit, QMessageBox
from PySide2.QtCore import QMimeData, QObject, Signal, Slot  
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt

from ci_substatEdit import SubstatEdit

import sys
from scripts.artifact import *

import numpy as np

class ArtifactWidget(QFrame):
    artifactSelectedSignal = Signal()
    artifactSavedSignal = Signal(Artifact)
    
    def __init__(self):
        super().__init__()
        
        # State
        self.selected = False
        
        # Static widgets
        buttonLayout = QHBoxLayout()
        self.clearbtn = QPushButton("Clear")
        buttonLayout.addWidget(self.clearbtn)
        self.clearbtn.clicked.connect(self.reset)
        
        self.savebtn = QPushButton("Save")
        buttonLayout.addWidget(self.savebtn)
        self.savebtn.clicked.connect(self.on_savebtn_pressed)
        
        self.labeltext = "Paste your artifact image here."
        self.label = QLabel(self.labeltext)
        
        self._widgetlayout = QVBoxLayout()
        self._widgetlayout.addLayout(buttonLayout)
        self._widgetlayout.addWidget(self.label)
        self.setLayout(self._widgetlayout)
        
        # Define available stats and create dropdowns (in derived classes)
        self.mainstatstrs = [] # this must be redefined per child class
        self.substatstrs = ['']
        allstatstrs = Artifact.getStatString() # get the dictionary of strings
        self.substatstrs.extend(list(v for k,v in allstatstrs.items() if "main" not in k))
        
        # call makeMainDropdown() and makeSubDropdowns() in children
        self.maindropdown = None
        self.mainedit = None
        self.subdropdowns = None
        self.subedits = None
    
    #%% Required reimplementations (virtuals)
    @Slot()
    def on_savebtn_pressed(self):
        # Main stat
        maindict = self.processMainStatEdit()
        # Substats (need handling because repeat substats not handled by class)
        subdict = self.processSubstatEdits() # handling done in derived classes

        # Return everything in one dict
        return {**maindict, **subdict}
    
    #%% Overrides
    def focusInEvent(self, event):
        print("this widget is focused")
        super().focusInEvent(event)
    
    def mousePressEvent(self, event):
        if not self.selected:
            self.select()
            self.artifactSelectedSignal.emit()
        else:
            self.deselect()
        
    #%%
    @Slot()
    def select(self):
        self.selected = True
        self.setStyleSheet("ArtifactWidget{  \
                           border: 1px solid black; \
                           }")
    
    @Slot()
    def deselect(self):
        self.selected = False
        self.setStyleSheet("ArtifactWidget{\
                           border: 0px solid black;\
                           }")
    
    @Slot()
    def reset(self):
        self.label.clear() # this should remove the image as well
        self.label.setText(self.labeltext)
        self.maindropdown.setCurrentIndex(0)
        self.mainedit.setText("")
        for i in range(len(self.subedits)):
            self.subedits[i].setText("")
            self.subedits[i].setEnabled(False)
            self.subdropdowns[i].setCurrentIndex(0)
    
    @Slot(QImage)
    def pasteImage(self, img):
        self.label.setPixmap(QPixmap.fromImage(img))
        self.label.setText("")
            
    def makeMainDropdown(self):
        dropdown = QComboBox(self)
        dropdown.addItems(self.mainstatstrs)
        
        self._widgetlayout.addWidget(dropdown)
        
        # Line Edits
        edit = QLineEdit()
        self._widgetlayout.addWidget(edit)

        # divider line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self._widgetlayout.addWidget(line)
        
        return dropdown, edit
        
    def makeSubDropdowns(self):
        subdropdowns = []
        subedits = []
        for i in range(4):
            subdd = QComboBox()
            subdd.addItems(self.substatstrs)
            subdropdowns.append(subdd)
            
            subedit = SubstatEdit()
            subedit.setEnabled(False)
            subedits.append(subedit)
            
            # connect to the substatedit's slot
            subdd.activated.connect(subedit.on_subdropdown_Activated)
            
        for i in range(len(subdropdowns)):
            hlayout = QHBoxLayout()
            hlayout.addWidget(subdropdowns[i])
            hlayout.addWidget(subedits[i])
            self._widgetlayout.addLayout(hlayout)
 
        return subdropdowns, subedits
    
    def processMainStatEdit(self):
        mainstatstr = self.maindropdown.currentText()
        mainvalue = float(self.mainedit.text())
        maindict = {}
        
        mainkey = Artifact.getMainStatKey(mainstatstr)
        maindict[mainkey] = mainvalue
            
        return maindict
    
    # Substats are supposed to be unique anyway
    def processSubstatEdits(self):
        subdict = {}
        
        for i in range(len(self.subedits)):
            if self.subedits[i].isEnabled():
                # get the substat
                subtxt = self.subdropdowns[i].currentText()
                subval = float(self.subedits[i].text())

                # get the key
                subkey = Artifact.getSubStatKey(subtxt)
                if subkey in subdict.keys():
                    raise ValueError("Repeat substat not allowed.")

                subdict[subkey] = subval
                
        return subdict
    
    def loadArtifactStats(self, artifact):
        statdict = Artifact.getStatString(None)
        
        i = 0
        for key, string in statdict.items():
            if getattr(artifact, key) is not None:
                if "main" in key:
                    self.maindropdown.setCurrentText(string)
                    self.mainedit.setText(str(getattr(artifact, key)))
                else:
                    self.subdropdowns[i].setCurrentText(string)
                    self.subedits[i].setEnabled(True)
                    self.subedits[i].setText(str(getattr(artifact, key)))
                    i = i + 1
    
    def on_save_error(self, e):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Invalid Input")
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setText(str(e))
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec()
        

#%%
class FlowerWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Flower image here."
        
        # Define available stats
        self.mainstatstrs = list(Flower.getMainStatKey(None).keys())
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        try:
            # call the parent method
            fulldict = super().on_savebtn_pressed()
            
            # create the slot artifact
            flower = Flower.fromDictionary(fulldict)
            # emit the signal
            self.artifactSavedSignal.emit(flower)
            
            self.reset()
            
        except Exception as e:
            self.on_save_error(e)

#%%    
class FeatherWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Feather image here."

        # Define available stats
        self.mainstatstrs = list(Feather.getMainStatKey(None).keys())
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        try:
            # call the parent method
            fulldict = super().on_savebtn_pressed()
            
            # create the slot artifact
            feather = Feather.fromDictionary(fulldict)
            # emit the signal
            self.artifactSavedSignal.emit(feather)
            
            self.reset()
        except Exception as e:
            self.on_save_error(e)
        
#%%    
class TimepieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Timepiece image here."

        # Define available stats
        self.mainstatstrs = list(Timepiece.getMainStatKey(None).keys())
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()

        self.reset()        
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        try:
            # call the parent method
            fulldict = super().on_savebtn_pressed()
            
            # create the slot artifact
            timepiece = Timepiece.fromDictionary(fulldict)
            # emit the signal
            self.artifactSavedSignal.emit(timepiece)
            
            self.reset()
        except Exception as e:
            self.on_save_error(e)

#%%    
class GobletWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Goblet image here."
        
        # Define available stats
        self.mainstatstrs = list(Goblet.getMainStatKey(None).keys())
        
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        try:
            # call the parent method
            fulldict = super().on_savebtn_pressed()
            
            # create the slot artifact
            goblet = Goblet.fromDictionary(fulldict)
            # emit the signal
            self.artifactSavedSignal.emit(goblet)
            
            self.reset()
        except Exception as e:
            self.on_save_error(e)

#%%    
class HeadpieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Headpiece image here."
        
        # Define available stats
        self.mainstatstrs = list(Headpiece.getMainStatKey(None).keys())
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        try:
            # call the parent method
            fulldict = super().on_savebtn_pressed()
            
            # create the slot artifact
            headpiece = Headpiece.fromDictionary(fulldict)
            # emit the signal
            self.artifactSavedSignal.emit(headpiece)
            
            self.reset()
        except Exception as e:
            self.on_save_error(e)
