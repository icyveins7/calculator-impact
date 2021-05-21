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
        
        # Frames for each slot
        self.flowerframe = FlowerWidget()
        self.featherframe = FeatherWidget()
        self.timepieceframe = TimepieceWidget()
        self.gobletframe = GobletWidget()
        self.headpieceframe = HeadpieceWidget()
        self.artifactframelist = [self.flowerframe,self.featherframe,
                                  self.timepieceframe,self.gobletframe,
                                  self.headpieceframe]
        self.currentFrame = None
        
        # Add to the layout
        for frame in self.artifactframelist:
            self.centralLayout.addWidget(frame)
        
        # Connections
        for frame in self.artifactframelist:
            frame.artifactSelectedSignal.connect(self.deselectFrames)

         
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
                    self.currentFrame.pasteImage(img)
