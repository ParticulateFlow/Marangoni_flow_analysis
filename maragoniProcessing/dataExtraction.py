import numpy as np
import cv2

def centerAndAllDiameters(frame: np.ndarray) -> tuple:
    '''Takes a frame and exports the center and diameters'''

    if len(frame.shape) == 3:
        # convert to grayscale and otsu method
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    else:
        otsu = frame.copy()

    # smooth image
    kernel = np.ones((10,10))
    otsu = cv2.dilate(otsu, kernel)

    # Find contours
    cnts, _ = cv2.findContours(otsu, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = np.concatenate(cnts) # Concatenate all contours -> to get the outer one

    # determine and draw bounding rectangle
    x, y, w, h = cv2.boundingRect(cnts)
    center = (int(x+w/2), int(y+h/2))
    rs = np.min([int(w/2),int(h/2)])

    # convert to polar coordinates
    polar_image = cv2.warpPolar(
            src=otsu,
            center=center,
            dsize=(rs,otsu.shape[1]),
            maxRadius=rs, 
            flags=cv2.WARP_FILL_OUTLIERS)

    # chnage data type and calculate mean over columns
    polar_image = np.float32(polar_image)
    p_mean = np.mean(polar_image, axis=0, dtype=np.float32)

    # core diameter
    index_core = np.where(p_mean == 255)[0]
    band_core = len(index_core)
    if band_core >= 15:
        rc = index_core[-1]
    else:
        rc = None

    # burst diameter
    index_burst= np.where(p_mean <= 20)[0]
    band_burst = len(index_burst)
    if band_burst >= 15:
        rb = index_burst[-1]
    else:
        rb = None

    return (center, rc, rb, rs)


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