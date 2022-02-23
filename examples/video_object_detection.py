from cv2 import cv2
from cv2 import data
import time
import numpy as np
from djitellopy import Tello
import matplotlib.pyplot as plt
#from find_face import findFace

font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

net = cv2.dnn.readNet('/home/bettylin2727/darknet/yolov3.weights', '/home/bettylin2727/darknet/cfg/yolov3.cfg')
classes = []
with open('/home/bettylin2727/darknet/data/coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0]- 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size =(len(classes), 3))

h, w = 720,960
fbRange = [20500, 19500]

tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()
# tello.takeoff()
# tello.send_rc_control(0, 0, 0, 25)


def findFace(img):
    
    faceCascade = cv2.CascadeClassifier(data.haarcascades + 'haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    myFaceListC = []
    myFaceListArea = []
 
    for (x, y, w, h) in faces:
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

 
    tello.send_rc_control(0, fb, int(-0.5*up_spd), speed)
 
    return error


while True:
    frame = tello.get_frame_read().frame
    height, width, channels = frame.shape  #maybe .shape() ?
    # detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320,320), (0,0,0), True, crop =False) #reduce to 320


    #cv2.resize(img, (w,h))
    #cv2.waitKey(5)
    #img, info = findFace(img)    
    #pError = trackFace( info, w, pid, pError)
    #print("Center", info[0], "Area", info[1])

    net.setInput(blob)
    outs = net.forward(outputlayers)
    # print(outs[1])

    # Showing info on screen
    # Get confidence score of algorithm in detecting an object in blob
    class_ids = []
    confidences= []
    boxes = []

    for out in outs :
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int (detection[0]*width)
                center_y = int (detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                x = int(center_x - w//2)
                y = int(center_y - h//2)
                # cv2.rectangle(img, ())

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id) #name of the object that was detected
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x+w, y+h), color , 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y+30), font, 1, (255,255,255), 2)

    elapsed_time = time.time() - starting_time
    fps = frame_id/ elapsed_time
    cv2.putText(frame, 'FPS:' + str(round(fps, 2)), (10,50), font, 2, (0,0,0), 1)

    cv2.imshow('Image', frame)
    key =cv2.waitKey(1)


    if (0xFF == ord('q')) or (key == 27):
        #tello.land()
        break

cv2. destoryAllWindows()

    