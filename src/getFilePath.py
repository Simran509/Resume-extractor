from inspect import getfile
import tkinter as tk

from tkinter import filedialog
from tkinter.filedialog import askopenfile

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # create window
        self.filename = "" # variable to store filename
        self.directoryName=""

        self.title("Resume Extractor")
        self.geometry("500x250")
        label = tk.Label(self, text="Click the Button to browse the CSV File", font=('Georgia 13'))
        label.pack(pady=10)
        tk.Button(self, text='Browse', command=self.openfile).pack()
        self.mainloop()

        tk.Tk.__init__(self) # create window
        self.title("Resume Extractor")
        self.geometry("500x250")
        label = tk.Label(self, text="Save the Resume Zip File in: (Select Folder)", font=('Georgia 13'))
        label.pack(pady=10)
        tk.Button(self, text='Browse', command=self.getDirectory).pack()
        self.mainloop()
        

    def openfile(self):
        self.filename =filedialog.askopenfile(title="open file", mode='r', filetypes=[('csv files', '*.csv'),])
        self.destroy()
        
    def getDirectory(self):
        # get a directory path by user
        self.directoryName=filepath=filedialog.askdirectory(initialdir=r"",
                                        title="Dialog box")
        label_path=tk.Label(self,text=filepath,font=('italic 14'))
        label_path.pack(pady=20)
        self.destroy()


    def getDirectoryPath(self):
        return(self.directoryName)

    def getFilePath(self):
        return(self.filename.name)
  
# #  FOR TESTING
# nap=App()

# ResumeFolder=nap.getFilePath()
# print(ResumeFolder)

# ResumeFolder=nap.getDirectoryPath()
# print(ResumeFolder)
