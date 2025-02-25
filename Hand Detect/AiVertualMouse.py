import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy


#########################
wCam , hCam = 1200,800
pTime = 0
smoothing = 5
plocX,plocY = 0,0
clocX,clocY =0,0
count = 0
#########################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.HandDetector(maxHands=1)
wScr,hScr =autopy.screen.size()
print(wScr,hScr)
while True:


    # 1. Find the hand landmarks
    success , img = cap.read()
    img = detector.findHands(img)
    lmlist,bbox = detector.findPosition(img)
    cv2.rectangle(img,(340, 150),( 900,470), (255, 255, 255), 2)

    # 2. Get the tip and index of middle finger
    if len(lmlist) != 0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]


        #print(x1,y1,x2,y2)

    # 3. Check which finger is up
        fingers = detector.fingersUp()
        #print(fingers)
        # 4. Only Index Finger : Moving Mode
        if fingers[1]==1 and fingers[2]==0:

            # 5. Convert Coordinates
            x3 = np.interp(x1,(340,900),(0,wScr))
            y3 = np.interp(y1,(150,470), (0,hScr))

            # 6. Smoothen Values
            clocX = plocX +(x3 - plocX)/smoothing
            clocY = plocY + (y3 - plocY) / smoothing
            # 7. Move mouse
            autopy.mouse.move(wScr - clocX,clocY)
            cv2.circle(img ,(x1,y1),8,(100,100,200),  cv2.FILLED,3)
            plocX,plocY = clocX,clocY
            print(fingers)

        if fingers[0] == 0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 :
            count+=1
            if count >8:
                print(count)
                autopy.mouse.click()
                count =0

    img = cv2.flip(img, 2)
    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(155,0,155),3)
    # 12. Display
    cv2.imshow("Image",img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):

            break




