
import numpy as np
from tqdm import tqdm
import cv2
import pandas as pd
import os
# self written functions
from functions.diameters import burstingDiameter, spreadDiameter
from videoWriterClass import videoWriterClass

def diameterRadiusAsCSV(frame, frameIndex: int,  gap: int):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # Diameters
    _, radius_bd = burstingDiameter(bw=otsu)
    center, radius_sd = spreadDiameter(bw=otsu)
    if radius_bd == None:
        radius_bd = 0
    
    band = radius_sd-radius_bd

    # extract ring
    outer_mask = np.zeros(otsu.shape[:2], dtype="uint8")
    outer_mask = cv2.circle(outer_mask, center, radius_sd, 255, -1)
    inner_mask = np.zeros(otsu.shape[:2], dtype="uint8")
    inner_mask = cv2.circle(inner_mask, center, radius_bd, 255, -1)
    mask = np.subtract(outer_mask, inner_mask)
    otsu_masked = cv2.bitwise_and(otsu,mask)

    # change to polar coordinates
    otsu_masked = otsu_masked.astype(np.float32)
    polar_image = cv2.warpPolar(
            src=otsu_masked,
            center=center,
            dsize=(radius_sd,otsu_masked.shape[0]),
            maxRadius=radius_sd,
            flags=cv2.WARP_FILL_OUTLIERS)
    polar_image = polar_image.astype(np.uint8)

    # get d/r data
    data = []
    step = int(band/gap)
    for i,r in enumerate(range(radius_bd,radius_sd,step)):
        A = polar_image[:,r:r+step]
        _,_,stats,_ = cv2.connectedComponentsWithStats(A, 8, cv2.CV_32S)
        
        # exclude border
        stats = stats[1:,:] 

        # filter artefacts
        index = np.where(stats[:,cv2.CC_STAT_AREA] < 5)
        stats = np.delete(stats,index,axis=0)
        
        if stats.size != 0:   
            w = np.mean(np.asarray(stats[:,cv2.CC_STAT_WIDTH]), axis=0)
            h = np.mean(np.asarray(stats[:,cv2.CC_STAT_HEIGHT]), axis=0)      
            d = np.mean(np.asarray([w,h]),axis=0)
            # append to dataset
            data.append([int(r+step/2), int(d)])
    if len(data) == 0:
        return
    df = pd.DataFrame(data,columns=['r','d'])
    filename = os.path.join(os.getcwd(), 'Data', 'results', f"{frameIndex}_gap{gap}.csv")
    df.to_csv(filename, index=False)



myWriter = videoWriterClass()

for frameIndex, frame in tqdm(enumerate(myWriter)):
    if frameIndex % 50 == 0:
        diameterRadiusAsCSV(frame=frame, frameIndex=frameIndex, gap=10)
print('Done')