import cv2
import numpy as np
from videoWriterClass import videoWriterClass

def getOtsu(frameNumber: int, cropFlag: bool) -> np.ndarray:

    myWriter = videoWriterClass()
    img = myWriter.getSingleImage(frameNumber = frameNumber)
    
    if cropFlag:
        img = img[50:1000, 450:1400] # crop image
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    return output,otsu