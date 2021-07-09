from PySide2.QtCore import QObject, QThread, Signal, Slot

import mss
import numpy as np
from PIL import Image, ImageQt

import time

from scripts.ocr_backend_combined import generate_dict
from scripts.artifact import *

class ScreenWatchWorker(QObject):
    new_artifact = Signal(Artifact)
    finished = Signal()

    def __init__(self, width, height, tessapi_wrapper, get_autocapture):
        super(ScreenWatchWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.screen_width = width
        self.screen_height = height
        self.citaw = tessapi_wrapper
        self.get_autocapture = get_autocapture

    @Slot()
    def run(self):
        """Screen Capture"""
        self.autocapture = True
        with mss.mss() as sct:
            # Part of the screen to capture
            monitor = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}
            prev_data = None

            while True:
                
                if self.get_autocapture():
                    # Get raw pixels from the screen, save it to a Numpy array
                    sct_img = sct.grab(monitor)
                    pil_img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                    img = ImageQt.ImageQt(pil_img)
                    
                    # create the array from image
                    img_size = img.size()
                    buffer = img.constBits()
                    arr = np.ndarray(shape  = (img_size.height(), img_size.width(), img.depth()//8),
                                buffer = buffer, 
                                dtype  = np.uint8)
                    arr = arr[:,:,:3] # clip the A buffer off
                    
                    try:
                        results, myartifact, ax, image = generate_dict(arr, self.screen_height, self.screen_width, citaw=self.citaw) # api
                        # results,myartifact,ax,image = generate_dict(arr, currentHeight, currentWidth) # pytesseract
                        print(results)
                        print(myartifact)
                        if myartifact != prev_data:
                            self.new_artifact.emit(Artifact.fromDictionary(myartifact))
                        prev_data = myartifact
                    except ValueError as e:
                        print(e)
                time.sleep(1)
        
        self.finished.emit()
        print('finished')