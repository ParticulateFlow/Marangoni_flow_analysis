from functions.diameters import burstingDiameter, spreadDiameter
from videoWriterClass import videoWriterClass

import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

def get_hist(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        _, radius_bd = burstingDiameter(bw=otsu)
        center, radius_sd = spreadDiameter(bw=otsu)

        # logic mask
        outer_mask = np.zeros(otsu.shape[:2], dtype="uint8")
        outer_mask = cv2.circle(outer_mask, center, radius_sd, 255, -1)
        inner_mask = np.zeros(otsu.shape[:2], dtype="uint8")
        inner_mask = cv2.circle(inner_mask, center, radius_bd, 255, -1)
        mask = np.subtract(outer_mask, inner_mask)

        otsu_masked = cv2.bitwise_and(otsu,mask)

        cnts, _ = cv2.findContours(otsu_masked, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas = np.asarray([cv2.contourArea(c) for c in cnts])
        index = list(np.where(areas == 0))
        areas = np.delete(areas, index, axis=0)

       
        # make a Figure and attach it to a canvas.
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasAgg(fig)

        # Do some plotting here
        ax = fig.add_subplot(111)
        ax.hist(areas)

        # Retrieve a view on the renderer buffer
        canvas.draw()
        buf = canvas.buffer_rgba()
        # convert to a NumPy array
        img = np.asarray(buf)

        img = cv2.resize(img, otsu.shape, interpolation = cv2.INTER_AREA)
        img = img[:,:,0:3]
        
        return img

def otsu(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return otsu

myWriter = videoWriterClass(suffix='hello')
myWriter.creatOutputVideo(fcn = get_hist)