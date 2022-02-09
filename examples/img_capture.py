from cv2 import cv2
from cv2 import data
import time
from djitellopy import Tello
import matplotlib.pyplot as plt
#from find_face import findFace

tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()


def findFace(img):
    
    # faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    faceCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_frontalface_default.xml')
    # smileCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_smile.xml')
    # faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    #smiles = smileCascade.detectMultiScale(imgGray, 1.2, 8)
    myFaceListC = []
    myFaceListArea = []
 

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




while True:
    img = tello.get_frame_read().frame
    cv2.resize(img, (360,240))
    #cv2.imshow("image", img)
    cv2.waitKey(5)
    # cv2.destroyAllWindows()

    # plt.figure()
    # plt.imshow(img)
    # plt.show()
    

    img, info = findFace(img)    

    #print()


    