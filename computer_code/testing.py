# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:23:29 2020

@author: Master Broda
"""

import time
#import dither
def time_function(func, img):
    start = time.time()
    func(img)
    return (time.time() - start)*1000