# -*- coding: utf-8 -*-
"""
Created on Sun May 30 13:36:15 2021

@author: Seo
"""

from PySide2.QtWidgets import QListWidget, QFrame, QVBoxLayout, QAbstractItemView
from PySide2.QtWidgets import QPushButton, QComboBox, QHBoxLayout
from PySide2.QtCore import QMimeData, QObject, Signal, Slot  
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt

import sys
sys.path.append("../scripts")
from artifact import Artifact
from artifact_slots import Flower, Feather, Timepiece, Goblet, Headpiece
from artifact_db import ArtifactDB

class ArtifactListFrame(QFrame):
    def __init__(self, con):
        super().__init__()
        
        # Stylesheeting
        self.setStyleSheet("ArtifactListFrame{border-width: 0px;}")
        self.setFixedWidth(192)

        self._widgetlayout = QVBoxLayout()
        self._widgetlayout.setContentsMargins(2,0,0,0)
        self.setLayout(self._widgetlayout)
        
        # Create filter dropdown
        self.filterDropdown = QComboBox()
        self.filterDropdown.addItems(['All','Flowers','Feathers',
                                      'Timepieces','Goblets','Headpieces'])
        
        # Create clear button
        self.clearbtn = QPushButton("Clear All")
        
        # Create the ListWidget
        self.artifactlistwidget = ArtifactListWidget(con)
        
        # Set up the layouts
        self.toplayout = QHBoxLayout()
        self.toplayout.addWidget(self.filterDropdown)
        self.toplayout.addWidget(self.clearbtn)
        self._widgetlayout.addLayout(self.toplayout)
        self._widgetlayout.addWidget(self.artifactlistwidget)
        
        # Connections
        self.clearbtn.clicked.connect(self.artifactlistwidget.clearArtifacts)
        self.filterDropdown.textActivated.connect(self.artifactlistwidget.filterArtifacts)

class ArtifactListWidget(QListWidget):
    insertResponseSignal = Signal(list, int)
    def __init__(self, con):
        super().__init__()
        # Initialize the table
        self.con = con
        self.db = ArtifactDB(self.con)
        self.artifacts = []
        self.ids = []
        # Load on init
        self.load()

        # Set selection mode
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
    @Slot()
    def load(self):
        self.clear()
        self.artifacts, self.ids = self.db.load(self.con)
        # Populate the list with loaded artifacts
        for artifact in self.artifacts:
            self.addItem(artifact.print())
        
    @Slot(int)
    def getSelected(self, idx):
        print("Got idx " + str(idx))
        selection = self.selectedIndexes()
        selectionRowIdx = [i.row() for i in selection]
        print(selectionRowIdx)
        artifactsSelected = [self.artifacts[i] for i in selectionRowIdx]
        print(artifactsSelected)
        self.insertResponseSignal.emit(artifactsSelected, idx)
    
    @Slot()
    def clearArtifacts(self):
        self.clear()
        self.db.clearTable(self.con)
        self.artifacts = []
        self.ids = []
    
    @Slot(Artifact)
    def addArtifact(self, artifact):
        self.db.save(artifact, self.con)
        self.load() # refresh artifacts and ids
        
    @Slot(str)
    def filterArtifacts(self, filterstr):
        print('landed in slot')
        filtered = None
        if filterstr == 'All':
            filtered = self.artifacts
        elif filterstr == 'Flowers':
            filtered = [i for i in self.artifacts if i.type==1]
        elif filterstr == 'Feathers':
            filtered = [i for i in self.artifacts if i.type==2]
        elif filterstr == 'Timepieces':
            filtered = [i for i in self.artifacts if i.type==3]
        elif filterstr == 'Goblets':
            filtered = [i for i in self.artifacts if i.type==4]
        elif filterstr == 'Headpieces':
            filtered = [i for i in self.artifacts if i.type==5]
            
        self.clear()
        for artifact in filtered:
            self.addItem(artifact.print())
            
            