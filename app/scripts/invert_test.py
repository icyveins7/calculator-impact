# -*- coding: utf-8 -*-
"""
Created on Mon May 17 00:24:50 2021

@author: Seo
"""

import pytesseract as tes
from PIL import Image
from PIL import ImageFilter
import PIL.ImageOps
import numpy as np

im = Image.open("../imgs/full.png")
im = im.convert("RGB") # the RGBAs are irrelevant anyway
otxt = tes.image_to_string(im, lang='eng', config='--oem 0')
print(otxt.strip())

inverted = PIL.ImageOps.invert(im)
ftxt = tes.image_to_string(inverted, lang='eng', config='--oem 0')
print(ftxt.strip())