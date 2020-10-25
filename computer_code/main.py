# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:23:13 2020

@author: Master Broda
"""

import cv2
import pafy
import numpy as np
from time import sleep
from time import time
import serial
import dither
import fast_dither
from dtsis_metrics import fps
import math
#url = "https://www.youtube.com/watch?v=zEMt3qViMjk"
url = "https://www.youtube.com/watch?v=RgKAFK5djSk"
#url = "https://www.youtube.com/watch?v=t0XN-dJftSU"
#url = 'https://www.youtube.com/watch?v=ugsvk7gLFNY'
#url = 'https://www.youtube.com/watch?v=90DN0Q1jWag'
url = 'https://www.youtube.com/watch?v=eFK7Iy8enqM'
url = 'https://www.youtube.com/watch?v=kJQP7kiw5Fk'





#video = pafy.new(url)
#best = video.getbest(preftype="mp4")

#capture = cv2.VideoCapture()
capture = cv2.VideoCapture('video_cut.mp4')
#capture.open(best.url)
i = 0
magic = b'\xde\xea\xdb\xee\xef'


def image_to_byte_array(img):
    byte_array = bytearray();
    for x in range(8): 
        for y in range(128):
            subarray = img[(x*8):(x*8)+8,y]
            byte = 0x00
            for i in range(8):
                if(subarray[7 - i]):
                    byte = byte | 0x01
                byte = byte << 1
            byte = byte >> 1
            byte_array.extend(byte.to_bytes(1,'little'))
    return byte_array


    
def black_white(img,thresh):
    ret = np.zeros(img.shape)
    ret[img>thresh] = 1
    return ret




def show_small_image(img):
    scaling_factor = 4
    show = cv2.resize(img,(img.shape[1]*scaling_factor,img.shape[0]*scaling_factor))
    cv2.imshow('window',show)
    
fps_counter = fps()
    
ser = serial.Serial('COM30',1000000)

ret = True
image_processing_time = 0;
frame_time = 0
wait_time = 0

while capture.isOpened():
    
    ret, frame = capture.read()
    fps_counter.update()
    if ret:
        start = time()

        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(grayscale, (64*2,32*2))

        i = i + 1
        if not i % 10:
            print(fps_counter.get_fps(),frame_time*1000)
    
        if not i % 1:
            ser.write(magic)
            #thresh = np.average(small)
            #out = black_white(small,thresh)
            
            #out = black_white(dither.hist_eq(dither.quantize(small)), 128)
            #out = black_white(dither.hist_eq(fast_dither.quantize(small)), 128)
            
            #out = black_white(dither.hist_eq(dither.stucki(small)), 128)
            out = black_white(fast_dither.stucki(dither.hist_eq(small)), 128)

            #out = dither.fake_grayscale(small)
            #out = fast_dither.fake_grayscale(small)
            #in_var = small.copy()
            #out = black_white(dither.stucki(in_var), 128)
            #image_processing_time = time() - start
            ser.write(image_to_byte_array(out))
        cv2.imshow('window', frame) 
        #show_small_image(out)
        if cv2.waitKey(5) & 0xff == ord('q'):
            break
        frame_time = time() - start
        wait_time = 1/30 - frame_time - 1/60
        if(wait_time < 0):
            wait_time = 0
        sleep(wait_time)

    else:
        break

capture.release()
cv2.destroyAllWindows()
ser.close()
    

                