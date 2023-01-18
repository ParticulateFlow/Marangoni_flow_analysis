
from tqdm import tqdm
import cv2
import numpy as np
import matplotlib.pyplot as plt

# self written functions
from functions.getOtsu import getOtsu
from functions.diameters import spreadDiameter, burstingDiameter, coreDiameter
from functions.markDiameter import markDiameter
from functions.rgb_colors import red,green,blue


input_filename = "Data/video_trim.mov"
output_filename = "Data/YUHU.mp4"


cap = cv2.VideoCapture(input_filename)
if not cap.isOpened():
    print('Cannot open video - Script aborted')
    exit(1)

vidFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT ))
vidFOURC = cv2.VideoWriter_fourcc(*'h264')
vidFPS = int(cap.get(cv2.CAP_PROP_FPS))
video = cv2.VideoWriter(output_filename, vidFOURC, vidFPS, (950,950))

# Read until video is completed
pbar = tqdm(total=vidFrames)
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    frame = frame[50:1000, 450:1400] # crop image
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    c_sd, r_sd = spreadDiameter(bw=otsu)
    c_cd, r_cd = coreDiameter(bw=otsu)
    c_bd, r_bd = burstingDiameter(bw=otsu)

    kernel = np.ones((20,20))
    #bw = cv2.dilate(otsu, kernel)
    #frame = cv2.cvtColor(bw, cv2.COLOR_GRAY2RGB)
    frame = markDiameter(image=frame, center=c_sd, radius=r_sd, color=red)
    frame = markDiameter(image=frame, center=c_cd, radius=r_cd, color=green)
    frame = markDiameter(image=frame, center=c_bd, radius=r_bd, color=blue)

    if th != None:
      video.write(frame)
    else:
      print('cannot convert to dilate image')
      break

  
  # Break the loop
  else:
    print('cannot open video')
    break

  # update progress bar
  pbar.update(1)  

cap.release()
video.release()
print('Done')
