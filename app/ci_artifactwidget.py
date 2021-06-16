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

import numpy as np

class ArtifactWidget(QFrame):
    artifactSelectedSignal = Signal()
    artifactSavedSignal = Signal(Artifact)
    processImgSignal = Signal(np.ndarray)
    
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
        # create the array from image
        img_size = img.size()
        buffer = img.constBits()
        arr = np.ndarray(shape  = (img_size.height(), img_size.width(), img.depth()//8),
                     buffer = buffer, 
                     dtype  = np.uint8)
        arr = arr[:,:,:3] # clip the A buffer off
        self.processImgSignal.emit(arr)
            
        
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
    
    def loadArtifactStats(self, artifact):
        self.loadArtifactMainStats(artifact)
        self.loadArtifactSubStats(artifact)
    
    def loadArtifactMainStats(self, artifact):
        if artifact.mainhpraw is not None:
            self.maindropdown.setCurrentText("HP")
            self.mainedit.setText(str(artifact.mainhpraw))
        elif artifact.mainatkraw is not None:
            self.maindropdown.setCurrentText("ATK")
            self.mainedit.setText(str(artifact.mainatkraw))
        elif artifact.mainhpperc is not None:
            self.maindropdown.setCurrentText("HP%")
            self.mainedit.setText(str(artifact.mainhpperc))
        elif artifact.mainatkperc is not None:
            self.maindropdown.setCurrentText("ATK%")
            self.mainedit.setText(str(artifact.mainatkperc))
        elif artifact.maindefperc is not None:
            self.maindropdown.setCurrentText("DEF%")
            self.mainedit.setText(str(artifact.maindefperc))
        elif artifact.mainer is not None:
            self.maindropdown.setCurrentText("Energy Recharge")
            self.mainedit.setText(str(artifact.mainer))
        elif artifact.mainem is not None:
            self.maindropdown.setCurrentText("Elemental Mastery")
            self.mainedit.setText(str(artifact.mainer))
        elif artifact.maincritrate is not None:
            self.maindropdown.setCurrentText("CRIT Rate%")
            self.mainedit.setText(str(artifact.maincritrate))
        elif artifact.maincritdmg is not None:
            self.maindropdown.setCurrentText("CRIT DMG%")
            self.mainedit.setText(str(artifact.maincritdmg))
        elif artifact.mainhealing is not None:
            self.maindropdown.setCurrentText("Healing Bonus%")
            self.mainedit.setText(str(artifact.mainhealing))
        elif artifact.maincryo is not None:
            self.maindropdown.setCurrentText("Cryo DMG Bonus%")
            self.mainedit.setText(str(artifact.maincryo))
        elif artifact.mainanemo is not None:
            self.maindropdown.setCurrentText("Anemo DMG Bonus%")
            self.mainedit.setText(str(artifact.mainanemo))
        elif artifact.maingeo is not None:
            self.maindropdown.setCurrentText("Geo DMG Bonus%")
            self.mainedit.setText(str(artifact.maingeo))
        elif artifact.mainpyro is not None:
            self.maindropdown.setCurrentText("Pyro DMG Bonus%")
            self.mainedit.setText(str(artifact.mainpyro))
        elif artifact.mainhydro is not None:
            self.maindropdown.setCurrentText("Hydro DMG Bonus%")
            self.mainedit.setText(str(artifact.mainhydro))
        elif artifact.mainelec is not None:
            self.maindropdown.setCurrentText("Electro DMG Bonus%")
            self.mainedit.setText(str(artifact.mainelec))
        elif artifact.mainphys is not None:
            self.maindropdown.setCurrentText("Physical DMG Bonus%")
            self.mainedit.setText(str(artifact.mainphys))
            
    def loadArtifactSubStats(self, artifact):
        i = 0

        if artifact.atkraw is not None:
            self.subdropdowns[i].setCurrentText("ATK")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.atkraw))
            i = i + 1
        if artifact.atkperc is not None:
            self.subdropdowns[i].setCurrentText("ATK%")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.atkperc))
            i = i + 1
        if artifact.hpraw is not None:
            self.subdropdowns[i].setCurrentText("HP")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.hpraw))
            i = i + 1
        if artifact.hpperc is not None:
            self.subdropdowns[i].setCurrentText("HP%")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.hpperc))
            i = i + 1
        if artifact.critrate is not None:
            self.subdropdowns[i].setCurrentText("CRIT Rate%")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.critrate))
            i = i + 1
        if artifact.critdmg is not None:
            self.subdropdowns[i].setCurrentText("CRIT DMG%")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.critdmg))
            i = i + 1
        if artifact.em is not None:
            self.subdropdowns[i].setCurrentText("Elemental Mastery")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.em))
            i = i + 1
        if artifact.er is not None:
            self.subdropdowns[i].setCurrentText("Energy Recharge")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.er))
            i = i + 1
        if artifact.defraw is not None:
            self.subdropdowns[i].setCurrentText("DEF")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.defraw))
            i = i + 1
        if artifact.defperc is not None:
            self.subdropdowns[i].setCurrentText("DEF%")
            self.subedits[i].setEnabled(True)
            self.subedits[i].setText(str(artifact.defperc))
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
        self.mainstatstrs = ['HP']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
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
        self.mainstatstrs = ['ATK']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
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
        self.mainstatstrs = ['HP%','ATK%','DEF%','Energy Recharge','Elemental Mastery']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()

        self.reset()        
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
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
        self.mainstatstrs = ['HP%','ATK%','DEF%','Elemental Mastery',
                             'Cryo DMG Bonus%', 'Anemo DMG Bonus%', 'Geo DMG Bonus%', 'Pyro DMG Bonus%',
                             'Hydro DMG Bonus%', 'Electro DMG Bonus%', 'Physical DMG Bonus%']
        
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
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
        self.mainstatstrs = ['HP%','ATK%','DEF%','CRIT Rate%','CRIT DMG%','Healing Bonus%']
        # Call the dropdown creators
        self.maindropdown, self.mainedit = self.makeMainDropdown()
        self.subdropdowns, self.subedits = self.makeSubDropdowns()
        
        self.reset()
        
    #%% Virtuals
    @Slot()
    def on_savebtn_pressed(self):
        # call the parent method
        fulldict = super().on_savebtn_pressed()
        try:
            # create the slot artifact
            headpiece = Headpiece.fromDictionary(fulldict)
            # emit the signal
            self.artifactSavedSignal.emit(headpiece)
            
            self.reset()
        except Exception as e:
            self.on_save_error(e)
