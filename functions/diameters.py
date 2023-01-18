import numpy as np
import cv2

def centerAndAllDiameters(frame: np.ndarray) -> tuple:
    '''Takes a frame and exports the center and diameters'''

    # STATES
    # + droplet (r_sd, r_bd, r_cd)
    # + tranient (r_sd, r_bd)
    # + disappeared (r_sd)

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
    r_sd = np.min([int(w/2),int(h/2)])

    # convert to polar coordinates
    polar_image = cv2.warpPolar(
            src=otsu,
            center=center,
            dsize=(r_sd,otsu.shape[1]),
            maxRadius=r_sd, 
            flags=cv2.WARP_FILL_OUTLIERS)

    # chnage data type and calculate mean over columns
    polar_image = np.float32(polar_image)
    p_mean = np.mean(polar_image, axis=0, dtype=np.float32)

    # core diameter
    index_core = np.where(p_mean == 255)[0]
    band_core = len(index_core)
    if band_core >= 15:
        r_cd = index_core[-1]
    else:
        r_cd = None

    # burst diameter
    index_burst= np.where(p_mean <= 20)[0]
    band_burst = len(index_burst)
    if band_burst >= 15:
        r_bd = index_burst[-1]
    else:
        r_bd = None

    return (center, r_cd, r_bd, r_sd)