import cv2
import pickle
import numpy as np
import serial
import cvzone

#1473,868

width , height = 30, 72
#video feed
#cam = cv2.VideoCapture(0)
cam=cv2.VideoCapture('sv.mp4')
with open("CarParkPosition",'rb') as f:
        posList = pickle.load(f)

def checkParkingSpace(framepro):
    spacecount = 0
    for pos in posList:
        x,y = pos
        framecrop = framepro[y:y+height,x:x+width]
        count = cv2.countNonZero(framecrop)
        #cvzone.putTextRect(frame,str(count),(x,y+height-10),scale = 1,thickness = 1, offset = 0)

        if count<450:
            color = (0,255,0)
            thickness = 5
            spacecount += 1
        else:
            color = (0,0,255)
            thickness = 2

        cv2.rectangle(frame,pos,(pos[0] + width, pos[1] + height),color,thickness)
    cvzone.putTextRect(frame,f'Free: {spacecount}/{len(posList)}',(100,50),scale = 4,thickness = 5, offset = 20, colorR=(0,200,0))

    #cv2.imshow("cropped frame",framecrop)

while True:
    if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT):
        cam.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, frame = cam.read()
    framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frameblur = cv2.GaussianBlur(framegray,(3,3),1)
    frameThreshold = cv2.adaptiveThreshold(frameblur,225,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    framemedian = cv2.medianBlur(frameThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    framedialate = cv2.dilate(framemedian,kernel,iterations=1)

    checkParkingSpace(framedialate)

    #for pos in posList:
        
    cv2.imshow('Parking cam',frame)
    #cv2.imshow('Parking camblur',frameblur)
    #cv2.imshow('Parking camthereshold',frameThreshold)
    #cv2.imshow('Parking cammedian',framemedian)
    cv2.waitKey(150)

