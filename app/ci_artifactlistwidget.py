# -*- coding: utf-8 -*-
"""
Created on Sun May 30 13:36:15 2021

@author: Seo
"""

from PySide2.QtWidgets import QListWidget
from PySide2.QtCore import QMimeData, QObject, Signal, Slot  
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt

import sys
sys.path.append("../scripts")
from artifact_slots import Flower, Feather, Timepiece, Goblet, Headpiece
from artifact_db import ArtifactDB

class ArtifactListWidget(QListWidget):
    def __init__(self, con):
        # Initialize the table
        self.con = con
        self.db = ArtifactDB(self.con)
        
    def addArtifact(self, artifact):
        self.db.save(artifact, self.con)