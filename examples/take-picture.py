from cv2 import cv2
import time
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.streamon()
time.sleep(5)
frame_read = tello.get_frame_read()

#tello.takeoff()
cv2.imwrite("picture.png", frame_read.frame)

#tello.land()
