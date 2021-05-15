import cv2
import numpy as np
import time
import math
import random

from subprocess import call

cam = cv2.VideoCapture(0)

GRID_SIZE = 4

SAVE = False
direction = 1

cur = 3
counter = 0
row = 0
col = 3

while True:
    _,frame = cam.read()
    frame = cv2.flip(frame,1)
    roi = frame[80:400,200:648]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    cv2.imshow('roi',roi)
    # cv2.imshow('frame',frame)

    if SAVE:
        y = int((row + random.random()) * (1080 // GRID_SIZE))
        x = int((col + random.random()) * (1920 // GRID_SIZE))

        call('xdotool mousemove '+str(x)+' '+str(y),shell=True)
        # cv2.imwrite('./imgs/'+str(row)+'_'+str(col)+'_'+str(counter)+'.jpg',roi)

        counter += 1
        if (counter > 200):
            cur += 1
            counter = 0
            row = cur // GRID_SIZE
            col = cur % GRID_SIZE
            print('row:',row,'col:',col)
            SAVE = False
        
    
    k = cv2.waitKey(2)
    if k==27: break
    if k==32:
        SAVE = True
        # print('current cell:',cur)

cv2.destroyAllWindows()