from tqdm import tqdm
import cv2
from getFile import getFileNameAndOutput
 

class videoWriterClass:

    def __init__(self):
        (inputFilename, outputFilename) = getFileNameAndOutput()
        self.vidCapIn = cv2.VideoCapture(inputFilename)

        if not self.vidCapIn.isOpened():
           print('Cannot open video - Script aborted')
           exit(1)

        # create output video writer
        fourc = int(self.vidCapIn.get(cv2.CAP_PROP_FOURCC))
        fps = int(self.vidCapIn.get(cv2.CAP_PROP_FPS))
        width = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_WIDTH ))
        height = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_HEIGHT ))

        self.Nframes = int(self.vidCapIn.get(cv2.CAP_PROP_FRAME_COUNT ))
        self.vidCapOut = cv2.VideoWriter(str(outputFilename), fourc, fps, (width, height))
    
    def creatOutputVideo(self, fcn: callable) -> None:
        pbar = tqdm(total=self.Nframes)
        while(self.vidCapIn.isOpened()):
            ret, frame = self.vidCapIn.read() # Capture frame-by-frame
            frame = fcn(frame)
            if ret == True:
                self.vidCapOut.write(frame)
                pbar.update(1) # update progress bar            
            else: # Break the loop
                print('cannot open video')
                break     
        self.vidCapIn.release(), self.vidCapOut.release()

def otsu(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return otsu
    
test = videoWriterClass()
test.creatOutputVideo(otsu)