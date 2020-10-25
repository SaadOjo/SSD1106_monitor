# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:18:39 2020

@author: Master Broda
"""
import cv2
import numpy as np

def num_to_option(num):
    ret = int(np.floor(num*0.02))
    if ret > 4:
        ret = 4
    return ret

def quantize(im):  # Floyd-Steinberg METHOD of image dithering
    w1=7/16.0
    w2=3/16.0
    w3=5/16.0
    w4=1/16.0
    width, height = im.shape
    for y in range(0,height-1):
        for x in range(1,width-1):
            old_pixel=im[x,y]
            if old_pixel<127:
                new_pixel=0
            else:
                new_pixel=255
            im[x,y] = new_pixel
            quant_err=old_pixel-new_pixel
            
            im[x+1,y] = im[x+1,y]+quant_err*w1
            im[x-1,y+1] = im[x-1,y+1] +  quant_err*w2
            im[x,y+1] = im[x,y+1] +  quant_err * w3
            im[x+1,y+1] = im[x+1,y+1] +  quant_err * w4
            
    return im

def fake_grayscale(img):
    shape = img.shape
    ret = np.zeros(shape)
    options = np.array([[[0,0],[0,0]], [[0,0],[0,1]], [[0,1],[0,1]], [[0,1],[1,1]], [[1,1],[1,1]] ])
    small = cv2.resize(img,(64,32)) #retuens 32, 64 numpy array
    for i in range(32):
        for j in range(64):
            ret[i*2:i*2+2,j*2:j*2+2] = options[num_to_option(small[i,j]),:,:]
    return ret
    
def set_pixel(im,x,y,new):
	im[x,y]=new
    
    
def hist_eq(im):
	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
	cl1 = clahe.apply(im)
	return cl1

def stucki(im):   # stucki algorithm for image dithering
	w8= 8/42.0;
	w7=7/42.0;
	w5=5/42.0;
	w4= 4/42.0;
	w2=2/42.0;
	w1=1/42.0;
	width,height=im.shape
	for y in range(0,height-2):
		for x in range(0,width-2):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255	
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y, im[x+1,y] + w7 * quant_err);
			set_pixel(im,x+2,y, im[x+2,y]+ w5 * quant_err);
			set_pixel(im,x-2,y+1, im[x-2,y+1] + w2 * quant_err);
			set_pixel(im,x-1,y+1, im[x-1,y+1] + w4 * quant_err);
			set_pixel(im,x,y+1, im[x,y+1] + w8 * quant_err);
			set_pixel(im,x+1,y+1, im[x+1,y+1] + w4 * quant_err);
			set_pixel(im,x+2,y+1, im[x+2,y+1] + w2 * quant_err);
			set_pixel(im,x-2,y+2, im[x-2,y+2] + w1 * quant_err);
			set_pixel(im,x-1,y+2, im[x-1,y+2] + w2 * quant_err);
			set_pixel(im,x,y+2, im[x,y+2] + w4 * quant_err);
			set_pixel(im,x+1,y+2, im[x+1,y+2] + w2 * quant_err);
			set_pixel(im,x+2,y+2, im[x+2,y+2]+ w1 * quant_err);
	return im
