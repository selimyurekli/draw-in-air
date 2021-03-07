'''import cv2
import numpy as np

import keyboard
from win32api import GetSystemMetrics
import time
widthScreen = GetSystemMetrics(0)
heightScreen = GetSystemMetrics(1)

def nothing(x):
    pass


def openWindow(name,width):
    cv2.namedWindow(name,width)
    cv2.createTrackbar("upper hue",name,255,255,nothing)
    cv2.createTrackbar("upper sat",name, 255, 255, nothing)
    cv2.createTrackbar("upper value",name, 255, 255, nothing)
    cv2.createTrackbar("lower hue",name, 0, 255, nothing)
    cv2.createTrackbar("lower sat",name, 193, 255, nothing)
    cv2.createTrackbar("lower value",name, 111, 255, nothing)
    cv2.createTrackbar("R", name, 0, 255, nothing)
    cv2.createTrackbar("G", name, 0, 255, nothing)
    cv2.createTrackbar("B", name, 0, 255, nothing)
    cv2.createTrackbar("Thickness", name, 3, 7, nothing)

def getWindowValues(name):
    upper_hue = cv2.getTrackbarPos("upper hue",name)
    upper_sat = cv2.getTrackbarPos("upper sat",name)
    upper_value = cv2.getTrackbarPos("upper value",name)
    lower_hue = cv2.getTrackbarPos("lower hue",name)
    lower_sat = cv2.getTrackbarPos("lower sat",name)
    lower_value = cv2.getTrackbarPos("lower value",name)
    r = cv2.getTrackbarPos("R",name)
    g = cv2.getTrackbarPos("G",name)
    b = cv2.getTrackbarPos("B",name)
    th = cv2.getTrackbarPos("Thickness",name)


    return {"upper_hue":upper_hue,
            "upper_sat": upper_sat,
            "upper_value": upper_value,
            "lower_hue": lower_hue,
            "lower_sat": lower_sat,
            "lower_value": lower_value,
            "R": r,
            "G": g,
            "B": b,
            "Thickness":th}

def openWhiteWindow(width,height):
    cv2.namedWindow("whitepaper")
    cv2.resizeWindow("whitepaper",width,width)
    whitepaper = np.zeros([width,height,3],dtype=np.uint8)
    whitepaper.fill(255)

    return whitepaper


if __name__ == "__main__":
    openWindow("TRACKBAR MENU",400)
    cam  = cv2.VideoCapture(0)
    whitepaper = openWhiteWindow(480,600)
    tempx = -1
    tempy = -1
    active = False

    while (True):
       ret,frame = cam.read()
       frame= cv2.flip(frame, 1)

       hsvOfFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


       mydic = getWindowValues("TRACKBAR MENU")
       lower_bound = np.array([mydic["lower_hue"],mydic["lower_sat"],mydic["lower_value"]])
       upper_bound = np.array([mydic["upper_hue"],mydic["upper_sat"],mydic["upper_value"]])
       r = mydic["R"]
       g = mydic["G"]
       b = mydic["B"]
       th = mydic["Thickness"]
       mask = cv2.inRange(hsvOfFrame,lower_bound,upper_bound)
       kernel = np.ones((5, 5), np.uint8)
       mask = cv2.dilate(mask, kernel, iterations=1)
       mask = cv2.erode(mask, kernel, iterations=1)
       blurred =  cv2.blur(mask,(10,10))

       first_index = np.where(blurred==255)


       if(first_index[0].size!=0 and first_index[1].size !=0 and active):
           cv2.line(whitepaper,(tempx,tempy),(int(first_index[1][0]),int(first_index[0][0])),color=(r,g,b),thickness=th)
           tempx, tempy = int(first_index[1][0]), int(first_index[0][0])


       elif(first_index[0].size!=0 and first_index[1].size !=0 and not active):
           tempx, tempy = int(first_index[1][0]), int(first_index[0][0])


       cv2.imshow("whitepaper", whitepaper)
       cv2.imshow("frame", blurred)


       if keyboard.is_pressed('a'):
           active = True


       elif keyboard.is_pressed('d'):
           active= False

       elif keyboard.is_pressed('s'):
           cv2.imwrite("filename.jpg",whitepaper)
           break
       elif keyboard.is_pressed('c'):
           whitepaper = np.zeros([480, 600], dtype=np.uint8)
           whitepaper.fill(255)
       if cv2.waitKey(1) & 0xFF ==ord('q'):
           break

    cam.release()
    cv2.destroyAllWindows()'''

