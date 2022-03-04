from cv2 import cv2
from cv2 import data
import time
import numpy as np
from djitellopy import Tello
import matplotlib.pyplot as plt

'''
ref: 
https://www.computervision.zone/courses/drone-programming-course/
https://djitellopy.readthedocs.io/en/latest/tello/
'''



h, w = 720,960
#fbRange = [20500, 19500]
fbRange = [19500, 20500]
pid = [0.1, 0.1, 0]
pError = 0


tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()
tello.takeoff()
#tello.send_rc_control(0, 0, 0, 25)


def findFace(img):
    
    faceCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_frontalface_default.xml')
    # eyeCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_eye.xml')
    # smileCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_smile.xml')

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    #eyes = eyeCascade.detectMultiScale(imgGray, 1.2, 8)
    #smiles = smileCascade.detectMultiScale(imgGray, 1.2, 8)
    myFaceListC = []
    myFaceListArea = []
 

    # x, y are the coordinates of the upper left detected bounding box 
    # w: width, h: height of bounding box
    for (x, y, w, h) in faces:

        # draw an rectangle for the bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # center of the bounding box
        cx = x + w // 2
        cy = y + h // 2
        area = w * h

        # draw a circle on the center
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), 2)
        print(cx, cy, area)
        
        # List of the Face centers
        myFaceListC.append([cx, cy])
        # List of the bounding box area
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
    # update yaw velocity : speed
    error = x - w // 2
    # PD controller
    speed = pid[0] * error + pid[1] * (error - pError)
    # speed constraints
    speed = int(np.clip(speed, -100, 100))

    # update up velocity : up_spd
    err_up = y - h // 3
    # PD controller
    up_spd = pid[0] * err_up + pid[1] * (err_up - pError)
    # constraints
    up_spd = int(np.clip(up_spd, -100, 100))


    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
 
    # when it's too near the face: go backward
    elif area > fbRange[1]:
        fb = -20
 
    # when it's too far away : go forward
    elif area < fbRange[0] and area != 0:
        fb = 20
 
    if x == 0:
        speed = 0
        error = 0
 
    #print(speed, fb)
 
    # send_rc_control(left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity)
    tello.send_rc_control(0, fb, int(-0.5*up_spd), speed)
 
    return error


while True:
    img = tello.get_frame_read().frame
    cv2.resize(img, (w,h))
    cv2.waitKey(5)

    img, info = findFace(img)    
    pError = trackFace( info, w, pid, pError)
    print("Center", info[0], "Area", info[1])

    # I usually use Ctrl+C in terminal to quit
    if 0xFF == ord('q'):
        tello.land()
        break

    