from cv2 import cv2
from cv2 import data
import time
import numpy as np
from djitellopy import Tello
import matplotlib.pyplot as plt
#from find_face import findFace


h, w = 720,960
#fbRange = [6200, 6800]
fbRange = [20500, 19500]
pid = [0.1, 0.1, 0]
pError = 0


tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()
tello.takeoff()
#tello.send_rc_control(0, 0, 0, 25)


def findFace(img):
    
    # faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    faceCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_frontalface_default.xml')
    # eyeCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_eye.xml')
    # smileCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_smile.xml')
    # faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print('imgGray size:', imgGray.shape)
    #print('img size:', img.shape)
    #imgGray = cv2.resize(imgGray, (360,240))
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    #eyes = eyeCascade.detectMultiScale(imgGray, 1.2, 8)
    #smiles = smileCascade.detectMultiScale(imgGray, 1.2, 8)
    myFaceListC = []
    myFaceListArea = []
 
        #for (x, y, w, h) in eyes:
    for (x, y, w, h) in faces:
        #for (x, y, w, h) in smiles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), 2)
        print(cx, cy, area)
        
 
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    cv2.imshow("image", img)
 
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
 
    else:
        return img, [[0, 0], 0]



def trackFace( info, w, pid, pError):
 
    area = info[1]
    x, y = info[0]
    fb = 0
    # update yaw velocity
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    # update up velocity
    err_up = y - h // 3
    up_spd = pid[0] * err_up + pid[1] * (err_up - pError)
    up_spd = int(np.clip(up_spd, -100, 100))



 
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
 
    elif area > fbRange[1]:
        fb = -20
 
    elif area < fbRange[0] and area != 0:
        fb = 20
 
    if x == 0:
        speed = 0
        error = 0
 
    #print(speed, fb)
 
    tello.send_rc_control(0, fb, int(-0.5*up_spd), speed)
 
    return error


while True:
    img = tello.get_frame_read().frame
    cv2.resize(img, (w,h))
    #cv2.imshow("image", img)
    cv2.waitKey(5)
    # cv2.destroyAllWindows()

    # plt.figure()
    # plt.imshow(img)
    # plt.show()
    

    img, info = findFace(img)    
    pError = trackFace( info, w, pid, pError)
    print("Center", info[0], "Area", info[1])

    if 0xFF == ord('q'):
        tello.land()
        break

    