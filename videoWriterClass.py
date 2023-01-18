from tqdm import tqdm
import cv2
import numpy as np
from functions.getFile import fileNameHandler
 

class videoWriterClass:
    def __init__(self):
        '''Opens the video with the help of a file handler'''
        self.fHandler = fileNameHandler()
        self.vidCapIn = cv2.VideoCapture(self.fHandler.inFilename)

        if not self.vidCapIn.isOpened():
           print('Cannot open video - Script aborted')
           exit(1)
            
    def creatOutputVideo(self, fcn: callable ,vidDim: tuple) -> None:
        '''creates an output video by a given warping function'''

        # creates the output video handler
        fourc = int(self.vidCapIn.get(cv2.CAP_PROP_FOURCC))
        fps = int(self.vidCapIn.get(cv2.CAP_PROP_FPS))
        if vidDim is None:
            # new video has same size as old video
            width = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_HEIGHT))
            vidDim = (width, height)
        self.Nframes = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_COUNT))

        try:
            self.vidCapOut = cv2.VideoWriter(self.fHandler.outFilename, fourc, fps, vidDim)
        except AttributeError:
            print("Add suffix to create an Ouptu Videowriter!")
        
        # iterate over video
        self.vidCapIn.set(cv2.CAP_PROP_POS_FRAMES, 0) # start at the beginning
        pbar = tqdm(total=self.Nframes)
        while(self.vidCapIn.isOpened()):
            ret, frame = self.vidCapIn.read() # Capture frame-by-frame
            if ret == True:
                frame = fcn(frame) # Do the transformation
                self.vidCapOut.write(frame)
                pbar.update(1) # update progress bar            
            else: # Break the loop
                print('cannot open video')
                break     
        self.vidCapIn.release(), self.vidCapOut.release()

            
    
    def getSingleImage(self, frameNumber: int) -> np.ndarray:
        self.vidCapIn.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
        ret, img = self.vidCapIn.read()
        if ret == True:
            return img
        else:
            print('Error no image found')
            return None
    
    def __iter__(self) -> np.ndarray:
        while(self.vidCapIn.isOpened()):
            ret, frame = self.vidCapIn.read() # Capture frame-by-frame
            if ret == True:
                yield frame
        yield StopIteration


#from functions.diameters import burstingDiameter, spreadDiameter
import seaborn as sns
import matplotlib as plt

if __name__ == '__main__':
    def myPolar(frame: np.ndarray) -> np.ndarray:
        
        (h,w) = frame.shape[0:2]
        center = (int(h/2), int(w/2))
        r = int(h/2)
        polar_image = cv2.warpPolar(
            src=frame,
            center=center,
            dsize=(w,h),
            maxRadius=r, 
            flags=cv2.WARP_FILL_OUTLIERS)
        return polar_image


    myWriter = videoWriterClass()
    img = myWriter.getSingleImage(frameNumber=0)
    (w,h) = img.shape[0:2]
    r = int(h/2)
    myWriter.creatOutputVideo(vidDim = (w,h), fcn = myPolar)
