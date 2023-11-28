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

#def find_picture(x,y,src,mat,threshold):
#    ret = False
#    w = mat.shape[1]
#    h = mat.shape[0]  
#    
#    src_crop = src[y:y+h,x:x+w].copy()            
#    
#    res = cv2.matchTemplate(src_crop,mat,cv2.TM_CCOEFF_NORMED)
#    #threshold = 0.9
#    loc = np.where( res >= threshold)
#    for pt in zip(*loc[::-1]):
#        #cv2.rectangle(src_img, pt, (pt[0] + mat_img.shape[1], pt[1] + mat_img.shape[0]), (0,0,255), 2)
#        print("found : ",pt)
#        ret = True
#
#    return ret
#    #cv2.imshow("crop", src_crop)
#    #cv2.imshow("match",mat)
#    #key = cv2.waitKey(0)
#   #cv2.destroyAllWindows()

class WindowCapture:

    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    _mouse_busy = False
    _mouse_delay = 0
    _mouse_event = []
    _mouse_ptr = 0

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        print(window_rect)
        print(self.w,self.h)
        print("window: {} , hwnd = {}".format(window_name, self.hwnd))

        # account for the window border and titlebar and cut them off
        border_pixels = 2
        titlebar_pixels = 32
        border_pixels = 0
        titlebar_pixels = 0

        #self.w = self.w - (border_pixels * 2)
        #self.h = self.h - titlebar_pixels - border_pixels
        print(self.w,self.h)

        #self.w = 720
        #self.h = 405
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y


    def get_screenshot(self):
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        #img = np.fromstring(signedIntsArray, dtype='uint8')
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[..., :3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img
        

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

    
    

