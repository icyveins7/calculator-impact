# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 23:07:12 2021

@author: Seo
"""

import os
import matplotlib.pyplot as plt
from skimage.io import imread


dirpath = "F:/PycharmProjects/calculator-impact-labelled"

filenames = os.listdir(dirpath)
imgfilenames = [i for i in filenames if '.png' in i]
txtfilenames = [i for i in filenames if '.txt' in i]
relabel = False

for i in range(len(imgfilenames)):
    
    imgfilepath = os.path.join(dirpath, filenames[i])
    print("Loading %s" % (imgfilepath))
    txtfilename = os.path.splitext(filenames[i])[0]+".txt"
    if txtfilename in txtfilenames and relabel is False:
        print("Already labelled, skipping")
        continue
    
    img = imread(imgfilepath)
    imgcols = img.shape[1]
    imgslice = img[:,int(2/3*imgcols):,:]
    
    plt.figure(1, figsize=(5,9))
    plt.ion()
    plt.clf()
    plt.imshow(imgslice)
    plt.show(block=False)
    
    instr = input()
    if instr == "exit":
        break
    
    # save input
    txtfilepath = os.path.join(dirpath, txtfilename)
    with open(txtfilepath, "w") as fp:
        fp.write(instr)
    print("Wrote to %s" % (txtfilepath))
    