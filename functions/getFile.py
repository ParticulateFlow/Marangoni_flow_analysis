import tkinter
from tkinter.filedialog import askopenfile
from pathlib import Path


class fileNameHandler():

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


if __name__ == '__main__':
    myFileHandler = fileNameHandler()
    print(myFileHandler.inFilename)
    print(myFileHandler.outFilename)

