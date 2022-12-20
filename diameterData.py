
import cv2
from tqdm import tqdm
import csv

# self written functions
from functions.diameters import centerAndAllDiameters
from videoWriterClass import videoWriterClass



myWriter = videoWriterClass()

for i,f in enumerate(myWriter):
    data = centerAndAllDiameters(f)
    print(f"{i}{data}")

