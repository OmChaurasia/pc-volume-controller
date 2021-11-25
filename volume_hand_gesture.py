import cv2
import mediapipe as mp
import time

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

from mediapipe.python.solutions import hands

vid= cv2.VideoCapture(0)
mpHands= mp.solutions.hands
hands= mpHands.Hands()
mpDraw= mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    ret, frame= vid.read()
    imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id , lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c= frame.shape
                cx,cy= int(lm.x*w), int(lm.y*h)

                # print(id,cx,cy)
                # to check the id of a point 
                if id == 0:
                    x0, y0=cx,cy
                if id == 5:
                    x5, y5=cx,cy
                if id == 4:
                    x4, y4=cx,cy
                if id ==8:
                    x8, y8=cx,cy
                    cv2.circle(frame,(cx,cy),10,(255,0,0),-1)
            handDistance= ((((x0 - x5 )**2) + ((y0-y5)**2) )**0.5)
            mainDistance= ((((x4 - x8 )**2) + ((y4-y8)**2) )**0.5)
            percentage= int(mainDistance *100 / (handDistance*3/2))
            if percentage>=100:
                percentage=100
            if percentage<=9:
                percentage=0
            cv2.putText(frame,str(f"Volume Percentage = {int(percentage)}"), (10,100),cv2.FONT_HERSHEY_SIMPLEX,0.7,(55,23,255),2)
            vol= -65.25-(-65.25*percentage/100)
            
            volume.SetMasterVolumeLevel(vol, None)
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)


    # fps tracking
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame,str(f"FPS = {int(fps)}"), (10,70),cv2.FONT_HERSHEY_SIMPLEX,0.7,(54,30,254),2)
    
    cv2.imshow("frame", frame)
    keyPressed = cv2.waitKey(10)
    if keyPressed == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()