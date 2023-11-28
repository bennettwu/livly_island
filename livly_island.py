# conda create --name livly_island python=3.9
# conda activate livly_island
# conda install pip
# pip install imutils pyautogui opencv-python numpy adbutils Pillow pywin32
import os, sys, time, random
import cv2
import numpy as np
from PIL import Image
import win32gui, win32api, win32ui, win32con, msvcrt
import imutils
from threading import Thread, Lock
import math
import subprocess

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


class   livly_island_matchtemplates:

    filelist = []
    imgs = []

    def __init__(self):
        self.filelist = [file for file in os.listdir('.') if file.endswith('.png')]
        print(self.filelist)
        for i in range(0, len(self.filelist)):
            print(self.filelist[i])
            img = cv2.imdecode(np.fromfile(self.filelist[i], dtype=np.uint8), 1)
            self.imgs.append(img)
        #print(self.filelist.index("None"))

    def get(self,filename):
        ## how to handle slef.imgs no contain filename??
        index = self.filelist.index(filename)
        return  self.imgs[index]

    def match(self,img):

        for i in range(0, len(self.filelist)):
            src_img = img
            mat_img = self.imgs[i]
            res = cv2.matchTemplate(src_img,mat_img,cv2.TM_CCOEFF_NORMED)
            threshold = float(0.98)
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(src_img, pt, (pt[0] + mat_img.shape[1], pt[1] + mat_img.shape[0]), (0,0,255), 2)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) < 2:
        print( "livly_island.py [window name]" )
        sys.exit()

    window_name = sys.argv[1]
    
    game = WindowCapture(window_name)
    game_matchtemplates = livly_island_matchtemplates()

    while(1):
        game_screen = game.get_screenshot()
        game_matchtemplates.match(game_screen)
        cv2.imshow("cap", cv2.resize(game_screen, (int(game_screen.shape[1] * 0.5), int(game_screen.shape[0] * 0.5)),interpolation=cv2.INTER_AREA) )
        if msvcrt.kbhit():
            ch =msvcrt.getch()
            #print(ch)
            if ch in [b'q', b'Q']:
                break
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        time.sleep(0.2)
    cv2.destroyAllWindows()        


