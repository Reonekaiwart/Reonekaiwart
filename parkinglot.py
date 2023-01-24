import cv2
import pickle




width , height = 35, 80

try:
    with open("CarParkPosition",'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouse_click(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    
    with open("CarParkPosition",'wb') as f:
        pickle.dump(posList,f)


while True:
    parking_img = cv2.imread('sp.png')
    #cv2.rectangle(parking_img,(55,305),(85,225),(255,0,255),2)
    for pos in posList:
        cv2.rectangle(parking_img,pos,(pos[0] + width, pos[1] + height),(255,0,255),2)
    cv2.imshow("Your Parking lot",parking_img)
    cv2.setMouseCallback("Your Parking lot",mouse_click)
    cv2.waitKey(1)
