# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 00:21:58 2021

@author: Seo
"""

from PySide2.QtWidgets import QGroupBox, QRadioButton, QVBoxLayout
from PySide2.QtCore import Signal, Slot  

class SettingsButton(QRadioButton):
    def __init__(self, text=None, imgfile="settings.png"):
        super().__init__(text)
        
        # Styling
        # <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
        self.setStyleSheet("QRadioButton::indicator{\
                           image: url(" + imgfile + ");\
                           width: 64px;\
                           height: 64px;\
                           border-width: 16px; \
                           border-style: solid; \
                           }\
                           QRadioButton::indicator::unchecked { \
                               background-color: rgb(240,240,240); \
                           } \
                            QRadioButton::indicator:unchecked:hover {\
                                background-color: rgb(230,230,230);\
                            }\
                            QRadioButton::indicator::checked {\
                                background-color: rgb(220,220,220);\
                            }")


class AddTabBtn(QRadioButton):
    def __init__(self, text=None, imgfile="edit.png"):
        super().__init__(text)
        
        # Styling
        # <div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
        self.setStyleSheet("QRadioButton::indicator{\
                           image: url(" + imgfile + ");\
                           width: 64px;\
                           height: 64px;\
                           border-width: 16px; \
                           border-style: solid; \
                           }\
                           QRadioButton::indicator::unchecked { \
                               background-color: rgb(240,240,240); \
                           } \
                            QRadioButton::indicator:unchecked:hover {\
                                background-color: rgb(230,230,230);\
                            }\
                            QRadioButton::indicator::checked {\
                                background-color: rgb(220,220,220);\
                            }")
                                
class CompareTabBtn(QRadioButton):
    def __init__(self, text=None, imgfile="compare.png"):
        super().__init__(text)
        
        # Styling
        # <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
        self.setStyleSheet("QRadioButton::indicator{\
                           image: url(" + imgfile + ");\
                           width: 64px;\
                           height: 64px;\
                           border-width: 16px; \
                           border-style: solid; \
                           }\
                           QRadioButton::indicator::unchecked { \
                               background-color: rgb(240,240,240); \
                           } \
                            QRadioButton::indicator:unchecked:hover {\
                                background-color: rgb(230,230,230);\
                            }\
                            QRadioButton::indicator::checked {\
                                background-color: rgb(220,220,220);\
                            }")
                           
#%%
class NavigationWidget(QGroupBox):
    def __init__(self):
        super().__init__(title=None)
        
        self.setContentsMargins(0,0,0,0)
        
        self._widgetlayout = QVBoxLayout()
        self._widgetlayout.setSpacing(0)
        self._widgetlayout.setContentsMargins(0,0,0,0)
        self.setLayout(self._widgetlayout)
        
        # Add buttons
        self.addTabBtn = AddTabBtn()
        self.cmpTabBtn = CompareTabBtn()
        self.settingsBtn = SettingsButton()
        
        self.addTabBtn.setChecked(True)
        
        self._widgetlayout.addWidget(self.addTabBtn)
        self._widgetlayout.addWidget(self.cmpTabBtn)
        self._widgetlayout.addWidget(self.settingsBtn)
        self._widgetlayout.insertStretch(-1)
        
        # Styling
        self.setMaximumWidth(96)
        self.setStyleSheet("QGroupBox{\
                           padding-right: -6px;\
                           border-width: 0px;\
                           }")
        