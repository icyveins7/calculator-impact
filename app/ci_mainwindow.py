# -*- coding: utf-8 -*-
"""
Created on Fri May 21 21:01:00 2021

@author: Seo
"""

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel
from PySide2.QtCore import QSize, QMimeData, QObject, Signal, Slot  
from PySide2.QtGui import QKeyEvent, QClipboard, QImage, QIcon
from PySide2.QtCore import Qt

from ci_artifactwidget import ArtifactWidget, FlowerWidget, FeatherWidget, TimepieceWidget, GobletWidget, HeadpieceWidget
from ci_artifactlistwidget import ArtifactListWidget, ArtifactListFrame
from ci_navigationwidget import NavigationWidget
from ci_settingsframe import SettingsFrame

import sqlite3 as sq

from string_filtering import generate_dict
import sys
import os
from artifact_slots import *
import warnings
from skimage.io import imread
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.getcwd(), "..","cpp"))
sys.path.append(os.path.join(os.getcwd(), "..","scripts"))
cwd = os.path.dirname(os.path.abspath(__file__))
tessdata_dir = os.path.join(cwd,"..","tesseract_custom")
os.environ["TESSDATA_PREFIX"] = tessdata_dir
print("Set TESSDATA_PREFIX to %s" % (os.environ["TESSDATA_PREFIX"]))
import tessapi_wrapper

class CIMainWindow(QMainWindow):
    # deselectFrameSignal = Signal()
    def __init__(self):
        super().__init__()
        
        # Window Details
        self.setWindowIcon(QIcon('Raccoon_Bear.png'))
        self.setWindowTitle("Calculator Impact")
        self.setMinimumSize(1366, 768)
        
        # Central Layout
        self._centralWidget = QWidget(self)
        self.centralLayout = QHBoxLayout()
        self._centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self._centralWidget)
        
        # Initialise Backend
        self.citaw = tessapi_wrapper.PyCITessApiWrapper()
        
        # Initialise database
        self.con = sq.connect("savedata.db")
        
        ### Settings Bar
        self.navbar = NavigationWidget()
        self.centralLayout.addWidget(self.navbar)
        
        ### List of artifacts
        self.artifactlistframe = ArtifactListFrame(self.con)
        self.artifactlist = self.artifactlistframe.artifactlistwidget
        # Add to layout
        self.centralLayout.addWidget(self.artifactlistframe)
        
        ### Frames for each slot
        self.flowerframe = FlowerWidget()
        self.featherframe = FeatherWidget()
        self.timepieceframe = TimepieceWidget()
        self.gobletframe = GobletWidget()
        self.headpieceframe = HeadpieceWidget()
        self.artifactframelist = [self.flowerframe,self.featherframe,
                                  self.timepieceframe,self.gobletframe,
                                  self.headpieceframe]
        self.currentFrame = None # for selecting which artifact to paste in
        
        # Add to the layout
        for frame in self.artifactframelist:
            self.centralLayout.addWidget(frame)
        
        ### Settings Frame (hidden on start)
        self.settingsFrame = SettingsFrame()
        self.centralLayout.addWidget(self.settingsFrame)
        self.settingsFrame.hide()


        ### Add stretch to layout after all frames
        self.centralLayout.addStretch(0)
        
        # Connections
        for frame in self.artifactframelist:
            frame.artifactSelectedSignal.connect(self.deselectFrames)
            frame.artifactSavedSignal.connect(self.artifactlist.addArtifact)
            frame.processImgSignal.connect(self.processImage)
        self.navbar.addTabBtn.clicked.connect(self.showAddTab)
        self.navbar.cmpTabBtn.clicked.connect(self.showCmpTab)
        self.navbar.settingsBtn.clicked.connect(self.showSettings)


    @Slot()
    def showAddTab(self):
        self.artifactlistframe.show()
        for frame in self.artifactframelist:
            frame.show()
        # hide everything else
        self.settingsFrame.hide()
        
    @Slot()
    def showCmpTab(self):
        print("Not implemented yet.")
        
    @Slot()
    def showSettings(self):
        self.settingsFrame.show()
        # hide everything else
        self.artifactlistframe.hide()
        for frame in self.artifactframelist:
            frame.hide()

    @Slot()
    def deselectFrames(self):
        for i in range(len(self.artifactframelist)):
            if self.sender() != self.artifactframelist[i]:
                self.artifactframelist[i].deselect()
            else:
                self.currentFrame = self.sender()
                
    @Slot(np.ndarray)
    def processImage(self, img):
        print("Landed in processImage slot")
        results,myartifact,ax,image = generate_dict(img, self.citaw)
        print(myartifact)
        self.sender().loadArtifactStats(Artifact.fromDictionary(myartifact)) # you don't actually need the type here, the saving will do it for you
    
    def keyPressEvent(self, e: QKeyEvent):
        super().keyPressEvent(e) # call the original one
        if (e.key() == Qt.Key_V and (e.modifiers() & Qt.ControlModifier)):
            print("CTRL-V pressed")
            
            clip = QApplication.clipboard()
            mime = clip.mimeData()
            
            # paste from file explorer
            if (mime.hasUrls()):
                print('mime has urls.')
            # paste from clipboard
            elif (mime.hasImage()):
                img = QImage(mime.imageData())
                if self.currentFrame is not None:
                    print("sending to frame")
                    self.currentFrame.pasteImage(img)
