# -*- coding: utf-8 -*-
"""
Created on Fri May 21 21:01:00 2021

@author: Seo
"""

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel
from PySide2.QtCore import QSize

class CIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window Details
        self.setWindowTitle("Calculator Impact")
        self.setMinimumSize(1366, 768)
        
        # Central Layout
        self._centralWidget = QWidget(self)
        self.centralLayout = QHBoxLayout()
        self._centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self._centralWidget)
        
        # Some placeholders
        for i in range(4):
            self.centralLayout.addWidget(QLabel("Test " + str(i)))