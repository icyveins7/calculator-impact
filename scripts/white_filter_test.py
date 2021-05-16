# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:37:16 2021

@author: Seo
"""

import pytesseract as tes
from PIL import Image
from PIL import ImageFilter
import numpy as np

im = Image.open("test_cut_oneline.png")
otxt = tes.image_to_string(im)
print(otxt.strip())

# numpy filtering

# pixdata = np.asarray(im)
# idx = np.where((pixdata==[255,255,255,255]).all(axis=2))
# newdata = np.zeros(pixdata.shape, pixdata.dtype)
# newdata[idx] = pixdata[idx] # only copy the white pixels, everything else is black
# newim = Image.fromarray(newdata)
# newim.save("white_filter_test.png")


# ftxt = tes.image_to_string(newim)


# print(ftxt.strip())

# PIL filtering, probably easier to read
source = im.split()

R, G, B = 0, 1, 2

# select regions where each colour is less than X
threshold = 230
for rgb in range(3):
    mask = source[rgb].point(lambda i: i < threshold and 255)
    
    # process the band to be black
    out = source[rgb].point(lambda i: i * 0)
    
    # paste the processed band back, but only where colour was < X
    source[rgb].paste(out, None, mask)

# build a new multiband image
newim = Image.merge(im.mode, source)

ftxt = tes.image_to_string(newim)
print(ftxt.strip())