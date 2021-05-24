# -*- coding: utf-8 -*-
"""
Created on Fri May 21 23:38:23 2021

@author: Seo
"""

# from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFrame, QVBoxLayout, QLabel, QComboBox
from PySide2.QtCore import QMimeData, QObject, Signal, Slot  
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt

class ArtifactWidget(QFrame):
    artifactSelectedSignal = Signal()
    def __init__(self):
        super().__init__()
        
        self.labeltext = "Paste your artifact image here."
        self.label = QLabel(self.labeltext)
        
        self._widgetlayout = QVBoxLayout()
        self._widgetlayout.addWidget(self.label)
        self.setLayout(self._widgetlayout)
        
        # Define available stats and create dropdowns (in derived classes)
        self.mainstatstrs = []
        self.substatstrs = ['ATK', 'ATK%', 'HP', 'HP%', 'CRIT Rate%',
                            'CRIT DMG%', 'Elemental Mastery', 'Energy Recharge',
                            'DEF', 'DEF%'] # mostly the same, so defined here
        # self.maindropdown = self.makeMainDropdown() # call these in children
        # self.subdropdowns = self.makeSubDropdowns()
    
    # override
    def focusInEvent(self, event):
        print("this widget is focused")
        super().focusInEvent(event)
    
    # override
    def mousePressEvent(self, event):
        print("clicked")
        self.setStyleSheet("border: 1px solid black;")
        self.artifactSelectedSignal.emit()
    
    @Slot()
    def deselect(self):
        self.setStyleSheet("border: 0px solid black;")
    
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
        
        return dropdown
        
    def makeSubDropdowns(self):
        subdropdowns = []
        for i in range(4):
            subdd = QComboBox()
            subdd.addItems(self.substatstrs)
            subdropdowns.append(subdd)
            
        for sub in subdropdowns:
            self._widgetlayout.addWidget(sub)
        
        return subdropdowns
    
#%%
class FlowerWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Flower image here."
        self.reset()
        
        # Define available stats
        self.mainstatstrs = ['HP']
        # Call the dropdown creators
        self.makeMainDropdown()
        self.makeSubDropdowns()

#%%    
class FeatherWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Feather image here."
        self.reset()

        # Define available stats
        self.mainstatstrs = ['ATK']
        # Call the dropdown creators
        self.makeMainDropdown()
        self.makeSubDropdowns()

#%%    
class TimepieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Timepiece image here."
        self.reset()
        
        # Define available stats
        self.mainstatstrs = ['HP%','ATK%','DEF%','Energy Recharge','Elemental Mastery']
        # Call the dropdown creators
        self.makeMainDropdown()
        self.makeSubDropdowns()

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
        self.makeMainDropdown()
        self.makeSubDropdowns()

#%%    
class HeadpieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Headpiece image here."
        self.reset()
        
        # Define available stats
        self.mainstatstrs = ['HP%','ATK%','DEF%','CRIT Rate%','CRIT DMG%','Healing Bonus%']
        # Call the dropdown creators
        self.makeMainDropdown()
        self.makeSubDropdowns()
