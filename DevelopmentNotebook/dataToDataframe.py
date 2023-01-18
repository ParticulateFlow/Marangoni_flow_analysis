
import cv2
from tqdm import tqdm
import csv

# self written functions
from functions.getOtsu import getOtsu
from functions.diameters import spreadDiameter, burstingDiameter, coreDiameter
from functions.markDiameter import markDiameter
from functions.rgb_colors import red,green,blue


input_filename = "Data/video_trim.mov"
output_filename = "data.csv"
cap = cv2.VideoCapture(input_filename)
if not cap.isOpened():
    print('Cannot open video - Script aborted')
    exit(1)

nFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['i','r_sd','r_bd','r_cd'])

    pbar = tqdm(total=nFrames)
    frameIndex = 0
    # Read until video is completed

    data = []
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            frame = frame[50:1000, 450:1400] # crop image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # Extract Parameters
            c_sd, r_sd = spreadDiameter(bw=otsu)
            c_bd, r_bd = burstingDiameter(bw=otsu)
            c_cd, r_cd = coreDiameter(bw=otsu)

            writer.writerow([frameIndex,r_sd,r_bd,r_cd])

        # Break the loop
        else:
            print('cannot open video')
            break
        pbar.update(1) 
        frameIndex += 1 

    cap.release()


