# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import string

correct = 'Elemental Mastery'
correctUp = correct.upper()

# generate possible error characters
errorChars = [i for i in string.ascii_uppercase]
errorChars.extend([i for i in string.punctuation])

# single errors
numIter = 100

# generate some indices
errorCharIdx = np.random.randint(0,len(errorChars),numIter)
errorCharIns = np.random.randint(0, len(correctUp),numIter)
errorInsOrReplace = np.random.randint(0,2,numIter)

# generate the error data 
errStrs = []
for i in range(numIter):
    err = correct.upper()
    ec = errorCharIdx[i]
    eci = errorCharIns[i]
    
    errStrs.append(err[:eci] + errorChars[ec] + err[eci:])
    
print(errStrs)
