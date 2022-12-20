from tqdm import tqdm
import cv2
import numpy as np
from functions.getFile import fileNameHandler
 

class videoWriterClass:
    def __init__(self):
        self.fHandler = fileNameHandler()
        self.vidCapIn = cv2.VideoCapture(self.fHandler.inFilename)

        if not self.vidCapIn.isOpened():
           print('Cannot open video - Script aborted')
           exit(1)
            
    def creatOutputVideo(self, fcn: callable ,vidDim: tuple) -> None:
        # create output video writer
        fourc = int(self.vidCapIn.get(cv2.CAP_PROP_FOURCC))
        fps = int(self.vidCapIn.get(cv2.CAP_PROP_FPS))
        if vidDim is None:
            width = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_HEIGHT))
            vidDim = (width, height)
        self.Nframes = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_COUNT))
        self.vidCapOut = cv2.VideoWriter(self.fHandler.outFilename, fourc, fps, vidDim)

        try:
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
        except AttributeError:
            print("Add suffix to create an Ouptu Videowriter!")
            
    
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


from functions.diameters import burstingDiameter, spreadDiameter
import seaborn as sns
import matplotlib as plt

if __name__ == '__main__':
    def myCropp(frame: np.ndarray) -> np.ndarray:
        return frame[50:1000, 450:1400,:] # crop image

    myWriter = videoWriterClass()
    myWriter.creatOutputVideo(vidDim = (950,950), fcn = myCropp)
