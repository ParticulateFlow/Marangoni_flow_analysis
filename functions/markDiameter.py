import numpy as np
import cv2
import matplotlib.pyplot as plt

def markDiameter(image: np.ndarray, center: tuple, radius: int, color: tuple) -> np.ndarray:
    
    lineThickness = 2
    markerSize = 50
     
    output = image.copy()
    
    if center is None:
        return output   

    # mark the circle on the image
    cv2.circle(
            img=output,
            center=center, 
            radius=radius,
            color=color,
            thickness=2)
    # mark the center
    cv2.drawMarker(
        img=output,
        position=center,
        color=color,
        markerType=cv2.MARKER_CROSS,
        markerSize=markerSize,
        thickness=lineThickness)

    return output

    