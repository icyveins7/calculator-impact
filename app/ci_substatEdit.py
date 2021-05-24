# -*- coding: utf-8 -*-
"""
Created on Mon May 24 23:41:47 2021

@author: Seo
"""

from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import Signal, Slot  

class SubstatEdit(QLineEdit):
    @Slot(int)
    def on_subdropdown_Activated(self, idx):
        if idx == 0:
            self.setEnabled(False)
        else:
            self.setEnabled(True)
            
            