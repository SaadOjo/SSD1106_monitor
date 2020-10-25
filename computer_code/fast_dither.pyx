# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:01:24 2020

@author: Master Broda
"""

import numpy as np
import cv2

cimport numpy as np

DTYPE = np.uint8

ctypedef np.uint8_t DTYPE_t

def num_to_option(num):
    cdef int ret = np.floor(num*0.02)
    if ret > 4:
        ret = 4
    return ret

def fake_grayscale(np.ndarray[DTYPE_t, ndim=2] img):
    
    cdef np.ndarray[DTYPE_t, ndim=3] options = np.array([ [[0,0],[0,0]], [[0,0],[0,1]], [[0,1],[0,1]], [[0,1],[1,1]], [[1,1],[1,1]] ], dtype=DTYPE)
    cdef int i,j
    cdef np.ndarray[DTYPE_t, ndim=2] small = cv2.resize(img,(64,32))
    cdef np.ndarray[DTYPE_t, ndim=2] ret = np.zeros((64,128),dtype=DTYPE)

    for j in range(64):
        for i in range(32):
            ret[(i*2):((i*2)+2),(j*2):((j*2)+2)] = options[num_to_option(small[i,j]),:,:]
    return ret
    

def quantize(np.ndarray[DTYPE_t, ndim=2] im):  # Floyd-Steinberg METHOD of image dithering
    cdef float w1=7/16.0
    cdef float w2=3/16.0
    cdef float w3=5/16.0
    cdef float w4=1/16.0
    cdef int width, height, x, y, quant_err
    
    #width, height = im.shape
    width = im.shape[0]
    height = im.shape[1]
    
    for y in range(0,height-1):
        for x in range(1,width-1):
            old_pixel=im[x,y]
            if old_pixel<127:
                new_pixel=0
            else:
                new_pixel=255
            im[x,y] = new_pixel
            quant_err=old_pixel-new_pixel
            
            im[x+1,y] = <int>(im[x+1,y]+quant_err*w1)
            im[x-1,y+1] = <int>(im[x-1,y+1] +  quant_err*w2)
            im[x,y+1] = <int>(im[x,y+1] +  quant_err * w3)
            im[x+1,y+1] = <int>(im[x+1,y+1] +  quant_err * w4)
            
    return im

def stucki(np.ndarray[DTYPE_t, ndim=2] im):   # stucki algorithm for image dithering
    cdef float w8 = 8/42.0
    cdef float w7 = 7/42.0
    cdef float w5 = 5/42.0
    cdef float w4 = 4/42.0
    cdef float w2 = 2/42.0
    cdef float w1 = 1/42.0
	
    cdef int width, height, x, y, old_pixel, new_pixel, quant_err
    
    width  = im.shape[0]
    height = im.shape[1]
    
    for y in range(0,height-2):
        for x in range(0,width-2):
            old_pixel=im[x,y]
            if old_pixel<127:
                new_pixel=0
            else:
                new_pixel=255	
            im[x,y] = new_pixel
            quant_err=old_pixel-new_pixel
            im[x+1,y] = <int>(im[x+1,y] + w7 * quant_err)
            im[x+2,y] = <int>(im[x+2,y]+ w5 * quant_err)
            im[x-2,y+1] = <int>(im[x-2,y+1] + w2 * quant_err)
            im[x-1,y+1] = <int>(im[x-1,y+1] + w4 * quant_err)
            im[x,y+1] = <int>(im[x,y+1] + w8 * quant_err)            
            im[x+1,y+1] = <int>(im[x+1,y+1] + w4 * quant_err)
            im[x+2,y+1] = <int>(im[x+2,y+1] + w2 * quant_err)
            im[x-2,y+2] = <int>(im[x-2,y+2] + w1 * quant_err)
            im[x-1,y+2] = <int>(im[x-1,y+2] + w2 * quant_err)
            im[x,y+2] = <int>(im[x,y+2] + w4 * quant_err)
            im[x+1,y+2] = <int>(im[x+1,y+2] + w2 * quant_err)
            im[x+2,y+2] = <int>(im[x+2,y+2]+ w1 * quant_err)
                        
            #set_pixel(im,x+1,y, im[x+1,y] + w7 * quant_err);
            #set_pixel(im,x+2,y, im[x+2,y]+ w5 * quant_err);
            #set_pixel(im,x-2,y+1, im[x-2,y+1] + w2 * quant_err);
            #set_pixel(im,x-1,y+1, im[x-1,y+1] + w4 * quant_err);
            #set_pixel(im,x,y+1, im[x,y+1] + w8 * quant_err);
            #set_pixel(im,x+1,y+1, im[x+1,y+1] + w4 * quant_err);
            #set_pixel(im,x+2,y+1, im[x+2,y+1] + w2 * quant_err);
            #set_pixel(im,x-2,y+2, im[x-2,y+2] + w1 * quant_err);
            #set_pixel(im,x-1,y+2, im[x-1,y+2] + w2 * quant_err);
            #set_pixel(im,x,y+2, im[x,y+2] + w4 * quant_err);
            #set_pixel(im,x+1,y+2, im[x+1,y+2] + w2 * quant_err);
            #set_pixel(im,x+2,y+2, im[x+2,y+2]+ w1 * quant_err);

    return im
