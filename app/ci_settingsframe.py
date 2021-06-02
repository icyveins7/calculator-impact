#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 10:35:46 2021

@author: seolubuntu
"""

from PySide2.QtWidgets import QFrame, QFormLayout, QComboBox
from PySide2.QtCore import Signal, SLOT

class SettingsFrame(QFrame):
    def __init__(self):
        super().__init__()
        
        self._widgetlayout = QFormLayout()
        self.setLayout(self._widgetlayout)
        
        # Call all grouped settings forms
        self.resDropdown = self.imgSettingsForm()
        
    def imgSettingsForm(self):
        resDropdown = QComboBox()
        resDropdown.addItems(['2560x1440','1920x1080'])
        
        self._widgetlayout.addRow("Resolution", resDropdown)
        
        return resDropdown
        