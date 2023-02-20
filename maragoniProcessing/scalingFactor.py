import cv2
import numpy as np

def scalingFactor(calib_img: np.ndarray, patternSize: tuple, checkerSize: int) -> tuple:
    '''returns the scaling factor and a varification image for calibration image
    Parameter:
        + calib_img: Calibration image with checkerboard on it
        + patternSize: number of intersections. CAVE=Gridsize-1
        + checkerSize: distance of intersections in mm'''
    
    img = calib_img.copy()
    if len(img.shape) >= 3: # convert to gray scale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(img, patternSize, None)

    if ret:
        # Euclidian norm between the first to corners
        d = np.linalg.norm(corners[1]-corners[0])
        # scaling factor
        scal = checkerSize/d

        # return overlayed edges
        corners = corners.astype(int)
        for c in corners:
            calib_img = cv2.drawMarker(
                calib_img, #img
                c[0], #position
                (0,255,0), #color
                cv2.MARKER_CROSS, #markerType
                50, #markerSize
                50) #thickness
    
        return (scal, calib_img)
    else:
        raise ValueError