# cv2 for computer vision
import cv2 
# A framework for building multimodal machine learning models
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
from mediapipe.python.solutions import hands
import numpy as np
import time
from pynput.keyboard import Key, Controller
import pydirectinput

# Time Delay this numbers just for initialization
up_delay= 100
right_delay=200
left_delay=200
down_delay=300

# Handling our video object, zero value mean camera number 1
# obj to simulate keuboard input
keyboard = Controller()
# obj to access webcam
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands 
hands = mpHands.Hands(min_detection_confidence=0.75)

while True:
    success,img = cap.read() #to read from webcam
    img = cv2.flip(img,1) # flip image horizontal
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Convert the frame from BGR to RGB color format
    results = hands.process(imgRGB) #to detect hand landmarks

    if results.multi_hand_landmarks:
        if len(results.multi_handedness)==2:
            pydirectinput.keyUp('down')
            pydirectinput.keyUp('left')
            pydirectinput.keyUp('right')
            pydirectinput.keyDown('up')
            up_delay = time.time()
            cv2.putText(img,'Both Hands',(250,50),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)
        else:
            for i in results.multi_handedness:
                label = MessageToDict(i)['classification'][0]['label']
                if label=='Left':
                    if (time.time()-left_delay) >= 1:
                        left_delay = time.time()
                        pydirectinput.keyUp('right')
                        pydirectinput.keyDown('left')
                        pydirectinput.keyDown('up')
                        cv2.putText(img,label+' Hand',(20,50),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)
                if label=='Right':
                    if (time.time()-right_delay) >= 1:
                        right_delay = time.time()
                        pydirectinput.keyUp('left')
                        pydirectinput.keyDown('right')
                        pydirectinput.keyDown('up')
                        cv2.putText(img,label+' Hand',(460,50),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)
                break
    
     # Handling Release buttons
    if (time.time()-down_delay)>2: 
        down_delay = time.time()
        pydirectinput.keyUp('down')
    if (time.time()-right_delay)>0.8:
        pydirectinput.keyUp('right')
    if (time.time()-left_delay)>0.8:
        pydirectinput.keyUp('left')
    if (time.time()-up_delay)>2:
        up_delay = time.time()
        pydirectinput.keyUp('up')

# 'q' is pressed, the loop breaks, and the program exits
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
         
    cv2.imshow('Image',img)
    cv2.waitKey(1)