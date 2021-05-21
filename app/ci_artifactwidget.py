# -*- coding: utf-8 -*-
"""
Created on Fri May 21 23:38:23 2021

@author: Seo
"""

# from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFrame, QVBoxLayout, QLabel
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
        
        # Define available stats
        self.mainstatstrs = []
        self.substatstrs = []
    
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
        
#%%
class FlowerWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Flower image here."
        self.reset()

#%%    
class FeatherWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Feather image here."
        self.reset()

#%%    
class TimepieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Timepiece image here."
        self.reset()

#%%    
class GobletWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Goblet image here."
        self.reset()

#%%    
class HeadpieceWidget(ArtifactWidget):
    def __init__(self):
        super().__init__()
        self.labeltext = "Paste your Headpiece image here."
        self.reset()
