# -*- coding: utf-8 -*-
"""
Created on Sun May 30 13:36:15 2021

@author: Seo
"""

from PySide2.QtWidgets import QListWidget, QFrame, QVBoxLayout
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
        self._widgetlayout = QVBoxLayout()
        self.setLayout(self._widgetlayout)
        
        # Create filter dropdown
        self.filterDropdown = QComboBox()
        
        # Create clear button
        self.clearbtn = QPushButton("Clear")
        
        # Create the ListWidget
        self.artifactlistwidget = ArtifactListWidget(con)
        
        # Set up the layouts
        self.toplayout = QHBoxLayout()
        self.toplayout.addWidget(self.filterDropdown)
        self.toplayout.addWidget(self.clearbtn)
        self._widgetlayout.addLayout(self.toplayout)
        self._widgetlayout.addWidget(self.artifactlistwidget)

class ArtifactListWidget(QListWidget):
    def __init__(self, con):
        super().__init__()
        # Initialize the table
        self.con = con
        self.db = ArtifactDB(self.con)
        self.artifacts = []
        self.ids = []
        # Load on init
        self.load()
        # Populate the list with loaded artifacts
        for artifact in self.artifacts:
            self.addItem(artifact.print())
        
    def load(self):
        self.artifacts, self.ids = self.db.load(self.con)
        
        
    @Slot(Artifact)
    def addArtifact(self, artifact):
        self.db.save(artifact, self.con)
        self.addItem(artifact.print())