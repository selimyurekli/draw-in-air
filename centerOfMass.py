import cv2
import numpy as np

import keyboard
from win32api import GetSystemMetrics


def nothing(x):
    pass


def openWindow(name,width):
    cv2.namedWindow(name,width)
    cv2.createTrackbar("upper hue",name,255,255,nothing)
    cv2.createTrackbar("upper sat",name, 255, 255, nothing)
    cv2.createTrackbar("upper value",name, 255, 255, nothing)
    cv2.createTrackbar("lower hue",name, 155, 255, nothing)
    cv2.createTrackbar("lower sat",name, 129, 255, nothing)
    cv2.createTrackbar("lower value",name, 127, 255, nothing)
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


    return {
            "upper_hue":upper_hue,
            "upper_sat": upper_sat,
            "upper_value": upper_value,
            "lower_hue": lower_hue,
            "lower_sat": lower_sat,
            "lower_value": lower_value,
            "R": r,
            "G": g,
            "B": b,
            "Thickness":th
           }

def openWhiteWindow(width,height):
    cv2.namedWindow("whitepaper")
    cv2.resizeWindow("whitepaper",width,width)
    whitepaper = np.zeros([width,height,3],dtype=np.uint8)
    whitepaper.fill(255)

    return whitepaper

def putTextToWhitePaper(whitepaper):
    cv2.putText(whitepaper,"Press 'A' to activate, 'D' to deactivate",(0,50),cv2.FONT_HERSHEY_PLAIN,fontScale=1.5,color=(0,0,0),thickness=2)
    cv2.putText(whitepaper,"Press 'C' to clean up, 'S' to save,'Q' to quit",(0,70),cv2.FONT_HERSHEY_PLAIN,color=(0,155,0),fontScale=1.5,thickness=2)


if __name__ == "__main__":
    openWindow("TRACKBAR MENU",400)
    cam  = cv2.VideoCapture(0)
    whitepaper = openWhiteWindow(480,600)
    putTextToWhitePaper(whitepaper)
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

        counters,_= cv2.findContours(blurred,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        if not counters:
            pass
        else:
            c = max(counters, key = cv2.contourArea)
            Center = cv2.moments(c)
            Cx = int(Center["m10"]/Center["m00"])
            Cy = int(Center["m01"]/Center["m00"])
            cv2.drawContours(frame, c, 1, color=(0, 245, 0), thickness=3)
            if active:
                cv2.circle(frame, (Cx, Cy), 2, (0, 255, 255), -1)

                cv2.line(whitepaper, (tempx, tempy), (Cx, Cy), color=(r, g, b),thickness=th)
                tempx, tempy =Cx,Cy
            else:
                tempx,tempy = Cx,Cy

        cv2.imshow("whitepaper", whitepaper)
        #cv2.imshow("blurred", blurred)
        cv2.imshow("frame",frame)


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
            putTextToWhitePaper(whitepaper)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

