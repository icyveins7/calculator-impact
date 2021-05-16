# -*- coding: utf-8 -*-
"""
Created on Mon May 17 00:33:24 2021

@author: Seo
"""

import pytesseract as tes
from PIL import Image
from PIL import ImageFilter
import PIL.ImageOps
import numpy as np

im = Image.open("../imgs/main_geodmg_oneline.png")
im = im.convert("RGB") # the RGBAs are irrelevant anyway
otxt = tes.image_to_string(im, lang='eng', config='--oem 0')
print(otxt.strip())

resizeFactors = np.arange(0.5,2.0,0.1)
for i in range(len(resizeFactors)):
    resized = im.resize((int(resizeFactors[i]*im.size[0]), int(resizeFactors[i]*im.size[1])))
    resized = PIL.ImageOps.invert(resized)
    ftxt = tes.image_to_string(resized, lang='eng', config='--oem 0')
    print("%.1f" % resizeFactors[i])
    print(ftxt.strip())