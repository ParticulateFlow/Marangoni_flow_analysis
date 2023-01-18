import numpy as np
import cv2
import sys # import requiered module
sys.path.append("..") # append the path of the parent directory
from functions.diameters import centerAndAllDiameters

def removeCore(bw: np.ndarray) -> np.ndarray:
    '''Remove the inner ring of a droplet'''

    center, _ , rb, rs = centerAndAllDiameters(frame=bw)

    # check if a droplet has a burst ring
    if rb == 0 or None:
        return bw
    
    # Calculate the outer ring
    outer_ring = np.zeros(bw.shape[:2], dtype="uint8")
    outer_ring = cv2.circle(outer_ring, center, rs, 255, -1)

    # Calculate the inner ring
    inner_ring = np.zeros(bw.shape[:2], dtype="uint8")
    inner_ring = cv2.circle(inner_ring, center, rb, 255, -1)

    # Combine both
    ring = np.subtract(outer_ring, inner_ring)

    # Apply and return
    bw_masked = cv2.bitwise_and(bw,ring)
    return bw_masked