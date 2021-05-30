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
sys.path.append("../scripts")
from artifact import Artifact
from artifact_slots import Flower, Feather, Timepiece, Goblet, Headpiece

class ArtifactWidget(QFrame):
    artifactSelectedSignal = Signal()
    artifactSavedSignal = Signal(Artifact)
    def __init__(self):
        super().__init__()
        
        # State
        self.selected = False
        
        # Static widgets
        self.savebtn = QPushButton("Save")
        self.savebtn.clicked.connect(self.on_savebtn_pressed)
        
        self.labeltext = "Paste your artifact image here."
        self.label = QLabel(self.labeltext)
        
        self._widgetlayout = QVBoxLayout()
        self._widgetlayout.addWidget(self.savebtn)
        self._widgetlayout.addWidget(self.label)
        self.setLayout(self._widgetlayout)
        
        # Define available stats and create dropdowns (in derived classes)
        self.mainstatstrs = [] # this must be redefined per child class
        self.substatstrs = ['', 'ATK', 'ATK%', 'HP', 'HP%', 'CRIT Rate%',
                            'CRIT DMG%', 'Elemental Mastery', 'Energy Recharge',
                            'DEF', 'DEF%'] # mostly the same, so defined here
        
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
        # Substats
        subdict = self.processSubstatEdits()
        
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
        self.label.setText(self.labeltext)
    
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
        
        if mainstatstr == "HP":
            maindict['mainhpraw'] = mainvalue
        elif mainstatstr == "ATK":
            maindict['mainatkraw'] = mainvalue
        elif mainstatstr == "HP%":
            maindict['mainhpperc'] = mainvalue
        elif mainstatstr == "ATK%":
            maindict['mainatkperc'] = mainvalue
        elif mainstatstr == "DEF%":
            maindict['maindefperc'] = mainvalue
        elif mainstatstr == "Energy Recharge":
            maindict['mainer'] = mainvalue
        elif mainstatstr == "Elemental Mastery":
            maindict['mainem'] = mainvalue
        elif mainstatstr == "CRIT Rate%":
            maindict['maincritrate'] = mainvalue
        elif mainstatstr == "CRIT DMG%":
            maindict['maincritdmg'] = mainvalue
        elif mainstatstr == "Healing Bonus%":
            maindict['mainhealing'] = mainvalue
        elif mainstatstr == "Cryo DMG Bonus%":
            maindict['maincryo'] = mainvalue
        elif mainstatstr == "Anemo DMG Bonus%":
            maindict['mainanemo'] = mainvalue
        elif mainstatstr == "Geo DMG Bonus%":
            maindict['maingeo'] = mainvalue
        elif mainstatstr == "Pyro DMG Bonus%":
            maindict['mainpyro'] = mainvalue
        elif mainstatstr == "Hydro DMG Bonus%":
            maindict['mainhydro'] = mainvalue
        elif mainstatstr == "Electro DMG Bonus%":
            maindict['mainelec'] = mainvalue
        elif mainstatstr == "Physical DMG Bonus%":
            maindict['mainphys'] = mainvalue
            
        return maindict
    
    # Substats are supposed to be unique anyway
    def processSubstatEdits(self):
        subdict = {}
        
        for i in range(len(self.subedits)):
            if self.subedits[i].isEnabled():
                # get the substat
                subtxt = self.subdropdowns[i].currentText()
                subval = float(self.subedits[i].text())
                
                # maintain this ordering
                if subtxt == 'ATK':
                    subdict['atkraw'] = subval
                elif subtxt == 'ATK%':
                    subdict['atkperc'] = subval
                elif subtxt == 'HP':
                    subdict['hpraw'] = subval
                elif subtxt == 'HP%':
                    subdict['hpperc'] = subval
                elif subtxt == 'CRIT Rate%':
                    subdict['critrate'] = subval
                elif subtxt == 'CRIT DMG%':
                    subdict['critdmg'] = subval
                elif subtxt == 'Elemental Mastery':
                    subdict['em'] = subval
                elif subtxt == 'Energy Recharge':
                    subdict['er'] = subval
                elif subtxt == 'DEF':
                    subdict['defraw'] = subval
                elif subtxt == 'DEF%':
                    subdict['defperc'] = subval
                
        return subdict
    
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
        self.reset()
        
        # Define available stats
        self.mainstatstrs = ['HP']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
            # create the slot artifact
            flower = Flower.fromDictionary(fulldict)
            # debug print to check
            flower.print()
            # emit the signal
            self.artifactSavedSignal.emit(flower)
            
        except Exception as e:
            self.on_save_error(e)

#%%    
class FeatherWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Feather image here."
        self.reset()

        # Define available stats
        self.mainstatstrs = ['ATK']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
            # create the slot artifact
            feather = Feather.fromDictionary(fulldict)
            # debug print to check
            feather.print()
            # emit the signal
            self.artifactSavedSignal.emit(feather)
        except Exception as e:
            self.on_save_error(e)
        
#%%    
class TimepieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Timepiece image here."
        self.reset()
        
        # Define available stats
        self.mainstatstrs = ['HP%','ATK%','DEF%','Energy Recharge','Elemental Mastery']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
            # create the slot artifact
            timepiece = Timepiece.fromDictionary(fulldict)
            # debug print to check
            timepiece.print()
            # emit the signal
            self.artifactSavedSignal.emit(timepiece)
        except Exception as e:
            self.on_save_error(e)

#%%    
class GobletWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Goblet image here."
        self.reset()
        
        # Define available stats
        self.mainstatstrs = ['HP%','ATK%','DEF%','Elemental Mastery',
                             'Cryo DMG Bonus%', 'Anemo DMG Bonus%', 'Geo DMG Bonus%', 'Pyro DMG Bonus%',
                             'Hydro DMG Bonus%', 'Electro DMG Bonus%', 'Physical DMG Bonus%']
        
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
            # create the slot artifact
            goblet = Goblet.fromDictionary(fulldict)
            # debug print to check
            goblet.print()
            # emit the signal
            self.artifactSavedSignal.emit(goblet)
        except Exception as e:
            self.on_save_error(e)

#%%    
class HeadpieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Headpiece image here."
        self.reset()
        
        # Define available stats
        self.mainstatstrs = ['HP%','ATK%','DEF%','CRIT Rate%','CRIT DMG%','Healing Bonus%']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
            # create the slot artifact
            headpiece = Headpiece.fromDictionary(fulldict)
            # debug print to check
            headpiece.print()
            # emit the signal
            self.artifactSavedSignal.emit(headpiece)
        except Exception as e:
            self.on_save_error(e)
