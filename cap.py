
import os, sys, time
#from windowcapture import WindowCapture
import cv2
import numpy as np
from PIL import Image
import win32gui, win32api, win32ui, win32con
import imutils
#import threading

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
    

