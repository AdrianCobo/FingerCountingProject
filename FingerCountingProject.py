import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionCon=0.9)
# thumb, index, midle finger, ringfinger, pinkyfinger
tipIds = [4, 8, 12, 16, 20]

while True:
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb (this condition is for the right hand).
        # You can check what hand it's and and adapt the code
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # rest fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1) # count how many 1 are on our list
        cv2.rectangle(img, (20,255), (170,425), (0,255,0, cv2.FILLED))
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # print the fps
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 255, 3))

    cv2.imshow("Image", img)
    cv2.waitKey(1)
