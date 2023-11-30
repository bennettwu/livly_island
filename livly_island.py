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
from windowcapture import WindowCapture


class   livly_island_matchtemplates:

    filelist = []
    imgs = []
    mx = -1
    my = -1
    mw = -1
    mh = -1

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

    def matchall(self,img):

        for i in range(0, len(self.filelist)):
            src_img = img
            mat_img = self.imgs[i]
            res = cv2.matchTemplate(src_img,mat_img,cv2.TM_CCOEFF_NORMED)
            threshold = float(0.98)
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                print("{} , {} , {} , w:{} h:{}".format(i, self.filelist[i] , pt , mat_img.shape[1] , mat_img.shape[0] ))
                cv2.rectangle(src_img, pt, (pt[0] + mat_img.shape[1], pt[1] + mat_img.shape[0]), (0,0,255), 2)

    def match(self,screen,sx,sy,filename,threshold):
        found = False
        index = self.filelist.index(filename)
        mat_img = self.imgs[index]
        w = mat_img.shape[1]
        h = mat_img.shape[0]
        if( sx == -1 or sy == -1 ):
            src_crop = screen
        else:
            src_crop = screen[sy:sy+h,sx:sx+w].copy()
        res = cv2.matchTemplate(src_crop,mat_img,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            x = pt[0]
            y = pt[1]
            if (sx == -1 or sy == -1):
                #cv2.rectangle(self.screen_result, (x, y), ((x + w), (y + h)), (0, 0, 255), 2)
                self.mx = -1
                self.my = -1
                self.mw = w
                self.mh = h
                found = True
            else:
                #cv2.rectangle(self.screen_result, (sx+x, sy+y), ((sx + x + w), (sy + y + h)), (0,0,255), 2)
                self.mx = x
                self.my = y
                self.mw = w
                self.mh = h
                found = True
        return found

    def match_result(self):
        return self.mx,self.my,self.mw,self.mh






if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) < 2:
        print( "livly_island.py [window name]" )
        sys.exit()

    window_name = sys.argv[1]
    
    game_window = WindowCapture(window_name)
    game_matchtemplates = livly_island_matchtemplates()

    idle = 0
    found = 0
    run = True    
    debug = True
    while(1):
        if( debug == True ):
            game_screen = game_window.get_screenshot()
            game_screen_matchall = game_screen.copy()
            game_matchtemplates.matchall(game_screen_matchall)
            cv2.imshow("All", cv2.resize(game_screen_matchall, (int(game_screen_matchall.shape[1] * 0.5), int(game_screen_matchall.shape[0] * 0.5)),interpolation=cv2.INTER_AREA) )

        if( run == True ):
            game_screen_match = game_screen.copy()
            if( game_matchtemplates.match(game_screen_match,150,598,"點擊並開始.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(150+(w/2),598+(h/2))
                #print(x,y,w,h,150+(w/2),598+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,153,599,"開始新生活.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                if( game_matchtemplates.match(game_screen_match,220,526,"同意.png",0.9) == True ):
                    x,y,w,h = game_matchtemplates.match_result()
                    game_window.click_left_mouse(220+(w/2),526+(h/2))
                else:
                    game_window.click_left_mouse(153+(w/2),599+(h/2))
                #print(x,y,w,h,153+(w/2),599+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,339,127,"下箭頭提示.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(339+(w/2)),int(127+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1

            elif( game_matchtemplates.match(game_screen_match,93,649,"開始生活!.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(93+(w/2)),int(649+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1

            elif( game_matchtemplates.match(game_screen_match,41,454,"輸入小島名稱.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(41+(w/2)),int(454+(h/2)))
                time.sleep(5)
                game_window.input_text("12345678")
                time.sleep(1)
                game_window.click_left_mouse(int(354),int(689))    
                time.sleep(1)
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,43,386,"輸入Livly名稱.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(43+(w/2)),int(386+(h/2)))
                time.sleep(5)
                game_window.input_text("12345678")
                time.sleep(1)
                game_window.click_left_mouse(int(354),int(689))    
                time.sleep(1)
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,42,318,"輸入飼主名稱.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(42+(w/2)),int(318+(h/2)))
                time.sleep(5)
                game_window.input_text("12345678")
                time.sleep(1)
                game_window.click_left_mouse(int(354),int(689))    
                time.sleep(1)
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,223,380,"是.png",0.98) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(223+(w/2)),int(380+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1                               
            elif( game_matchtemplates.match(game_screen_match,141,617,"同意飼主條款.png",0.98) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(141+(w/2)),int(617+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1               
            elif( game_matchtemplates.match(game_screen_match,90,649,"登錄.png",0.98) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(90+(w/2)),int(649+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1               
            elif( game_matchtemplates.match(game_screen_match,149,635,"前往小島.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(149+(w/2)),int(635+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,90,655,"下一步.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(90+(w/2)),int(655+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,143,183,"請選擇喜歡的個體.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(143+(w/2)),int(183+(h/2)+70))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,88,656,"決定此Livly種類.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(88+(w/2)),int(656+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,92,650,"繼續辨理手續.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(92+(w/2)),int(650+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,91,655,"迎接Livly.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(91+(w/2)),int(655+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            elif( game_matchtemplates.match(game_screen_match,26,340,"APK圖示.png",0.9) == True ):
                x,y,w,h = game_matchtemplates.match_result()
                game_window.click_left_mouse(int(26+(w/2)),int(340+(h/2)))
                #print(x,y,w,h,25+(w/2),340+(h/2))
                found += 1
            else:
                found = 0
                idle += 1

            print(idle,found)
            

        
        #cv2.imshow("Matchall", cv2.resize(game_screen, (int(game_screen.shape[1] * 0.5), int(game_screen.shape[0] * 0.5)),interpolation=cv2.INTER_AREA) )

        if msvcrt.kbhit():
            ch =msvcrt.getch()
            #print(ch)
            if ch in [b'q', b'Q']:
                break
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        time.sleep(0.1)
    cv2.destroyAllWindows()        


