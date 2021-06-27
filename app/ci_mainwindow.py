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
from ci_comparisonframe import ComparisonFrame

import sqlite3 as sq

from string_filtering import generate_dict
import sys
import os
from artifact_slots import *
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
        self.centralLayout.setSpacing(0)
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
        
        #### Comparison Frame (hidden on start)
        self.comparisonFrame = ComparisonFrame()
        self.centralLayout.addWidget(self.comparisonFrame)
        self.comparisonFrame.hide()


        ### Add stretch to layout after all frames
        # self.centralLayout.addStretch(0)
        
        # Connections
        for frame in self.artifactframelist:
            frame.artifactSelectedSignal.connect(self.deselectFrames)
            frame.artifactSavedSignal.connect(self.artifactlist.addArtifact)
        self.navbar.addTabBtn.clicked.connect(self.showAddTab)
        self.navbar.cmpTabBtn.clicked.connect(self.showCmpTab)
        self.navbar.settingsBtn.clicked.connect(self.showSettings)
        self.comparisonFrame.insertRequestSignal.connect(self.artifactlist.getSelected)
        self.artifactlist.insertResponseSignal.connect(self.comparisonFrame.insertArtifacts)


    @Slot()
    def showAddTab(self):
        self.artifactlistframe.show()
        for frame in self.artifactframelist:
            frame.show()
        # hide everything else
        self.settingsFrame.hide()
        self.comparisonFrame.hide()
        
    @Slot()
    def showCmpTab(self):
        self.artifactlistframe.show()
        self.comparisonFrame.show()
        # hide everything else
        for frame in self.artifactframelist:
            frame.hide()
        self.settingsFrame.hide()
        
    @Slot()
    def showSettings(self):
        self.settingsFrame.show()
        # hide everything else
        self.artifactlistframe.hide()
        for frame in self.artifactframelist:
            frame.hide()
        self.comparisonFrame.hide()

    @Slot()
    def deselectFrames(self):
        for i in range(len(self.artifactframelist)):
            if self.sender() != self.artifactframelist[i]:
                self.artifactframelist[i].deselect()
            else:
                self.currentFrame = self.sender()
                
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
                    # self.currentFrame.pasteImage(img)
                    
                    # create the array from image
                    img_size = img.size()
                    buffer = img.constBits()
                    arr = np.ndarray(shape  = (img_size.height(), img_size.width(), img.depth()//8),
                                 buffer = buffer, 
                                 dtype  = np.uint8)
                    arr = arr[:,:,:3] # clip the A buffer off
                    
                    # Get the resolution
                    currentResolution = self.settingsFrame.getResolution().split("x")
                    print("Resolution is ")
                    print(currentResolution)
                    currentHeight = int(currentResolution[1])
                    currentWidth = int(currentResolution[0])
                    
                    results,myartifact,ax,image = generate_dict(arr, currentHeight, currentWidth, citaw=self.citaw) # api
                    # results,myartifact,ax,image = generate_dict(arr, currentHeight, currentWidth) # pytesseract
                    print(results)
                    print(myartifact)
                    self.currentFrame.loadArtifactStats(Artifact.fromDictionary(myartifact)) # you don't actually need the type here, the saving will do it for you
                    
                    # recreate the qimage for display
                    image = np.copy(image[:,:,:3], order='C') # need to copy into c-contiguous
                    qimg = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
                    self.currentFrame.pasteImage(qimg)
                    
                    
    
