# -*- coding: utf-8 -*-
"""
Created on Sun May 16 12:37:16 2021

@author: Seo
"""

import pytesseract as tes
from PIL import Image
from PIL import ImageFilter
import numpy as np

im = Image.open("../imgs/main_geodmg_oneline.png")
im = im.convert("RGB")
otxt = tes.image_to_string(im, lang='eng', config='--oem 0')
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
threshold = 240
for rgb in range(3):
    blackmask = source[rgb].point(lambda i: i < threshold and 255)
    
    # process the band to be black
    out = source[rgb].point(lambda i: i * 0)
    
    # paste the processed band back, but only where colour was < X
    source[rgb].paste(out, None, blackmask)
    
    # whitemask = source[rgb].point(lambda i: i >= threshold and 255)
    
    # # process the band to be black
    # out = source[rgb].point(lambda i: 255)
    
    # # paste the processed band back, but only where colour was < X
    # source[rgb].paste(out, None, whitemask)
    

# build a new multiband image
newim = Image.merge(im.mode, source)
ftxt = tes.image_to_string(newim, lang='eng', config='--oem 0')
print(ftxt.strip())

# slice left half
newim_left = newim.crop((0,0,int(newim.size[0]/2),newim.size[1]))
ftxtleft = tes.image_to_string(newim_left, lang='eng', config='--oem 0')
print(ftxtleft.strip())

# slice right half
newim_right = newim.crop((int(newim.size[0]/2),0,newim.size[0],newim.size[1]))
ftxtright = tes.image_to_string(newim_right, lang='eng', config='--oem 0')
print(ftxtright.strip())