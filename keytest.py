import os, sys, time
import cv2
import numpy as np
from PIL import Image
import win32gui, win32api, win32ui, win32con
import imutils
import threading
import urllib
from windowcapture import WindowCapture


import win32gui
import win32api
import win32con
import time
import win32ui

def send_input_hax(hwnd, msg):
    for c in msg:
        if c == "\n":
        	pass
            #win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            #win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            print(ord(c))
            #win32api.PostMessage(hwnd, win32con.WM_KEYDOWN,ord(c) , 0)
            win32api.PostMessage(hwnd, win32con.WM_CHAR, ord(c), 0)
            time.sleep(0.05)
            #win32api.PostMessage(hwnd, win32con.WM_KEYUP, ord(c),0)

#hwnd = win32gui.FindWindow(None, "Untitled")
hwnd = win32gui.FindWindow(None, "*Untitled - Notepad")
hwnd = win32gui.FindWindow(None, "Livly Island")
print(hwnd)
if hwnd:
	print("Found")
	send_input_hax(hwnd,"12345")
else:
	print("Not Found")
#				win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParamMatch)
#			win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, None , lParamMatch)


