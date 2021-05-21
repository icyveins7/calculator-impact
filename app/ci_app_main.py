# -*- coding: utf-8 -*-
"""
Created on Fri May 21 20:57:17 2021

@author: Seo
"""

import sys
from PySide2.QtWidgets import QApplication
from ci_mainwindow import CIMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mainwindow = CIMainWindow()
    mainwindow.show()
    
    app.exec_()