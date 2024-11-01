import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self):
        self.filename = ""  # Variable to store filename
        self.directoryName = ""
        self.create_csv_window()

    def create_csv_window(self):
        self.csv_window = tk.Tk()  # Create a new window for the CSV file selection
        self.csv_window.title("Select CSV File")
        self.csv_window.geometry("500x250")
        
        label = tk.Label(self.csv_window, text="Click the Button to browse the CSV File", font=('Georgia', 13))
        label.pack(pady=10)
        
        tk.Button(self.csv_window, text='Browse CSV', command=self.openfile).pack(pady=10)

        self.csv_window.mainloop()

    def openfile(self):
        file = filedialog.askopenfile(title="Open CSV File", mode='r', filetypes=[('CSV files', '*.csv')])
        if file:
            self.filename = file.name
            print(f"Selected CSV File: {self.filename}")  # Feedback to user
            self.csv_window.destroy()  # Close the CSV selection window
            self.create_directory_window()  # Open the next window for directory selection

    def create_directory_window(self):
        self.dir_window = tk.Tk()  # Create a new window for directory selection
        self.dir_window.title("Select Output Directory")
        self.dir_window.geometry("500x250")
        
        label = tk.Label(self.dir_window, text="Select Folder to Save the Resume Zip File:", font=('Georgia', 13))
        label.pack(pady=10)
        
        tk.Button(self.dir_window, text='Browse Directory', command=self.getDirectory).pack(pady=10)

    def getDirectory(self):
        self.directoryName = filedialog.askdirectory(title="Select Output Directory")
        if self.directoryName:
            print(f"Selected Directory: {self.directoryName}")  # Feedback to user
            self.dir_window.destroy()  # Close the directory selection window

    def getFilePath(self):
        return self.filename

    def getDirectoryPath(self):
        return self.directoryName

# Testing (if needed, comment out in actual usage)
#if __name__ == '__main__':
#    app = App()
