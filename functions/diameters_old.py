import numpy as np
import cv2


def spreadDiameter(bw: np.ndarray) -> tuple:
    """Takes a binary image of the droplet and extracts the spread diameter"""

    # smoth the image a little bit
    kernel = np.ones((10,10))
    bw = cv2.dilate(bw, kernel)

    # Find contours
    cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Concatenate all contours -> to get the outer one
    cnts = np.concatenate(cnts)

    # # Determine and draw bounding rectangle
    x, y, w, h = cv2.boundingRect(cnts)
    center = (int(x+w/2), int(y+h/2))
    radius = np.min([int(w/2),int(h/2)])

    return (center, radius)


def burstingDiameter(bw: np.ndarray) -> tuple:
    """returns the bursting diameter (bd) of a droplet"""

    center_cd, radius_cd = coreDiameter(bw=bw)

    if center_cd is not None:
        mask = np.zeros(bw.shape[:2], dtype="uint8")
        mask = cv2.circle(mask, center_cd, radius_cd+5, 255, -1)
        bw = cv2.subtract(bw,mask)
    kernel = np.ones((30,30))
    bw = cv2.dilate(bw, kernel)

    contours,hierachies = cv2.findContours(bw, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    hierachies = hierachies[0]

    index = np.where(hierachies[:,3] < 0)
    contours = np.asarray(contours, dtype='object')
    f_cnt = np.delete(contours, index, axis=0)
    f_h = np.delete(hierachies, index, axis=0)

    if f_cnt.size == 0:
        return (None, None)

    circle,radius =circleApproximation(f_cnt[-1])

    #check if result is good
    imgSize = bw.size
    circleSize = radius**2 * 3.14

    if(circleSize/imgSize > 0.05):
        return (circle, radius)
    else:
        return (None, None)


def coreDiameter(bw: np.ndarray) -> tuple:
    """Takes a binary image of the droplet and extracts the core diameter (cd)"""

    # Find the contours
    contours,hierachies = cv2.findContours(bw, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    hierachies = hierachies[0] # get the actual inner list of hierarchy descriptions

    # Filter contours by area
    percent = 1 
    areaTH = int(bw.size*percent/100)

    filtered_hierachy, filtered_contour = [], []
    for cnt, h in zip(contours,hierachies):
        if cv2.contourArea(cnt)>areaTH:
            filtered_hierachy.append(h)
            filtered_contour.append(cnt)

    # check if lists contains elements
    if not filtered_contour:
        # no core diameter found
        return (None,None)

    # reorder everything to extract only the inner bloob
    if len(filtered_hierachy) > 1:
        filtered_hierachy = np.asarray(filtered_hierachy, dtype='object')
        index = list(np.where(filtered_hierachy[:,2] == -1))
        filtered_hierachy = np.delete(filtered_hierachy, index, axis=0)
        filtered_contour = np.asarray(filtered_contour, dtype='object')
        filtered_contour = np.delete(filtered_contour, index, axis = 0)

    # retrieve the contour approximation
    return circleApproximation(filtered_contour[-1])


## Helping functions

def circleApproximation(cnt: np.ndarray) -> tuple:
    '''After the searched contour is extracted the circle approximation
    could be retourned'''
    (x,y) ,r = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(r)
    return (center, radius)