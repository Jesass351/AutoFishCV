import cv2
import time
import numpy as np


cap = cv2.VideoCapture("test.mp4")
template = cv2.imread('test/fish_ico2.png')
last_x = 0
new_x = 0

direction = 0

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,800)
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 2
lineType               = 2

smoother_last_x = []
smoother_new_x = []

SMOOTH_FRAMES = 10

REGION_START_X = 20
REGION_END_X = 1900

REGION_START_Y = 180
REGION_END_Y = 500


while True:
    ret, frame = cap.read()

    height, width, _ = frame.shape

    region = frame[REGION_START_Y:REGION_END_Y, REGION_START_X: REGION_END_X]


    img_rgb = region

    w, h = template.shape[:-1]

    res = cv2.matchTemplate(region, template, cv2.TM_CCOEFF_NORMED)
    threshold = .67
    loc = np.where(res >= threshold)
    if loc[0].size != 0:
        for pt in zip(*loc[::-1]):  # поменять местами строки стобцы, они почему-то криво стоят
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)


            if len(smoother_new_x) != SMOOTH_FRAMES: #усредняю значения из каждых N кадров, тк рыба дёргается
                smoother_new_x.append(pt[0])
            else:
                new_x = sum(smoother_new_x) / len(smoother_new_x)
                smoother_new_x.clear()


            if len(smoother_last_x) != SMOOTH_FRAMES:
                smoother_last_x.append(new_x)
            else:
                last_x = sum(smoother_last_x) / len(smoother_last_x)
                smoother_last_x.clear()



            print(last_x, new_x, direction)


            if last_x > new_x:
                direction = 1
            elif last_x == new_x:
                direction = 0
            else:
                direction = -1

    cv2.putText(frame,str(direction), 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    thickness,
    lineType)

    cv2.rectangle(frame,(REGION_START_X,REGION_START_Y), (REGION_END_X, REGION_END_Y),(0,255,0), 1) 

    cv2.imshow("Frame", frame)


    key = cv2.waitKey(30)
    if key == 27:
        break





cap.release()
cv2.destroyAllWindows()