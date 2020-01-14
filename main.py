from tkinter import *

class loadingWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('250x250')
        self.window.overrideredirect(1)
        self.window.mainloop()

if __name__ == "__main__":
    loadingWindow()