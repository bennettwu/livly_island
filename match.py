#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, time
import cv2
import numpy as np
from PIL import Image
import win32gui, win32api, win32ui, win32con
import imutils
import threading
import urllib
from windowcapture import WindowCapture


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if len(sys.argv) < 4:
        print( "sdcap.py source_picture match.png threshold" )
        sys.exit()

    source_file = sys.argv[1]
    match_file = sys.argv[2]
    threshold_val = sys.argv[3] 
    
    #src_img = cv2.imread(source_file)
    #mat_img = cv2.imread(match_file)
    src_img = cv2.imdecode(np.fromfile(source_file, dtype=np.uint8), 1)
    mat_img = cv2.imdecode(np.fromfile(match_file, dtype=np.uint8), 1)
    print("src",src_img.shape)
    print("mat",mat_img.shape)
    #sdc = WindowCapture(window_name)
    #img = sdc.get_screenshot()

    #res = find_picture(506,110,src_img,mat_img,0.99)
    #print(res)

    #res = find_picture(506,110,src_img,mat_img,0.99)
    #print(res)
        
    s = time.time()
    res = cv2.matchTemplate(src_img,mat_img,cv2.TM_CCOEFF_NORMED)
    threshold = float(threshold_val)
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(src_img, pt, (pt[0] + mat_img.shape[1], pt[1] + mat_img.shape[0]), (0,0,255), 2)
        print("found : ",pt)
    e = time.time()
    print("time: " , e-s)
    
   
    cv2.imshow("result", src_img)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    

