from maragoniProcessing import *
import cv2

video = videoHandling.videoHandler()


for frame in video:
    print(dataExtraction.centerAndAllDiameters(frame))


# def otsu(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#     img = cv2.cvtColor(otsu, cv2.COLOR_GRAY2RGB)
#     return img


# video.creatOutputVideo(fcn=otsu, vidDim=None)


