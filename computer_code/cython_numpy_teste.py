# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:50:10 2020

@author: Master Broda
"""

import time
import numpy as np
import fast_dither
import dither
#import dither
def time_function(func, img):
    start = time.time()
    func(img)
    return (time.time() - start)*1000


img = np.zeros((64,128),dtype=np.uint8)

print(time_function(fast_dither.quantize,img))

print(time_function(dither.quantize,img))



