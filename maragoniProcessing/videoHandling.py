import tkinter
from tkinter.filedialog import askopenfile
from pathlib import Path
from tqdm import tqdm

import cv2
import numpy as np


class videoHandler():
    def __init__(self):
        '''Opens the video with the help of a file handler'''
        self.fHandler = filenameHandler()
        self.vidCapIn = cv2.VideoCapture(self.fHandler.inFilename)

        if not self.vidCapIn.isOpened():
           print('Cannot open video - Script aborted')
           exit(1)

        width = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.vidDim = (height, width)
            
    def creatOutputVideo(self, fcn: callable ,vidDim: tuple) -> None:
        '''creates an output video by a given warping function'''

        if vidDim is None:
            vidDim = self.vidDim

        # creates the output video handler
        fourcc = int(self.vidCapIn.get(cv2.CAP_PROP_FOURCC))
        #fourcc = cv2.VideoWriter_fourcc(*'')
        fps = int(self.vidCapIn.get(cv2.CAP_PROP_FPS))
        self.Nframes = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_COUNT))

        try:
            self.vidCapOut = cv2.VideoWriter(self.fHandler.outFilename, fourcc, fps, vidDim)
        except AttributeError:
            print("Add suffix to create an Ouptu Videowriter!")
        
        # iterate over video
        self.vidCapIn.set(cv2.CAP_PROP_POS_FRAMES, 0) # start at the beginning
        print('Start creating Video')
        pbar = tqdm(total=self.Nframes)
        while(self.vidCapIn.isOpened()):
            ret, frame = self.vidCapIn.read() # Capture frame-by-frame
            if ret == True:
                frame = fcn(frame) # Do the transformation
                self.vidCapOut.write(frame)
                pbar.update(1) # update progress bar            
            else: # Break the loop
                pbar.close()
                print('VideoWriter closed')
                break     
        self.vidCapIn.release(), self.vidCapOut.release()           
    
    def getSingleImage(self, frameNumber: int) -> np.ndarray:
        '''returns a frame selected by a frame number'''
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




class filenameHandler():
    def __init__(self) -> None:
        # open file dialog
        root = tkinter.Tk()
        root.withdraw()

        fname = askopenfile(title="Select Videofile")
        self.filename = Path(fname.name)

    @property
    def inFilename(self):
        return str(self.filename.absolute())

    @property
    def outFilename(self):
        fname = self.filename
        output = fname.with_name(f"{fname.stem}_out{fname.suffix}")
        return str(output.absolute())



## TEST my CLASS
if __name__ == '__main__':
    myHandler = filenameHandler()
    print(myHandler.inFilename)
    print(myHandler.outFilename)

  
    myWriter = videoHandler()
    img = myWriter.getSingleImage(frameNumber=0)
    (w,h) = img.shape[0:2]
    print(w)
    print(h)