
import os, sys, time
from windowcapture import WindowCapture
import cv2
import numpy as np
from PIL import Image
import win32gui, win32api, win32ui, win32con
import imutils


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if len(sys.argv) < 3:
        print( "sdcap.py [windows name] [outpu file.png]" )
        sys.exit()

    window_name = sys.argv[1]
    output_file = sys.argv[2]
    
    sdc = WindowCapture(window_name)
    img = sdc.get_screenshot()
    
    cv2.imshow("result", img)
    cv2.imwrite(output_file,img)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(output_file,img)
    

