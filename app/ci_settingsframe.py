#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 10:35:46 2021

@author: seolubuntu
"""

from PySide2.QtWidgets import QFrame, QFormLayout, QComboBox
from PySide2.QtCore import Signal, Slot

import json

class SettingsFrame(QFrame):
    def __init__(self):
        super().__init__()
        
        self._widgetlayout = QFormLayout()
        self.setLayout(self._widgetlayout)
        
        # Call all grouped settings forms
        self.resDropdown = self.imgSettingsForm()
        
        # Load from file
        try:
            self.readSettings()
        except:
            # Create the settings file
            self.writeSettings()
        
        # Connections
        self.resDropdown.currentTextChanged.connect(self.writeSettings)
        
    def imgSettingsForm(self):
        resDropdown = QComboBox()
        resDropdown.addItems(['2560x1440','1920x1080'])
        
        self._widgetlayout.addRow("Resolution", resDropdown)
        
        return resDropdown
        
    def getResolution(self):
        return self.resDropdown.currentText()
    
    @Slot()
    def writeSettings(self):
        print("Saving settings")
        with open("settings.json", "w") as f:
           settings = {}
           settings['resolution'] = self.getResolution()
           
           json.dump(settings, f)
           
    @Slot()
    def readSettings(self):
        print("Reading settings")
        with open("settings.json", "r") as f:
            settings = json.load(f)
            print(settings)
            
            self.resDropdown.setCurrentText(settings['resolution'])