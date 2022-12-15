import cv2
import numpy as np

def getOtsu(frameNumber: int) -> np.ndarray:

    cap = cv2.VideoCapture("Data/video_trim.mov")
    cap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
    _, img = cap.read()

    img = img[50:1000, 450:1400] # crop image

    output = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    return output,otsu