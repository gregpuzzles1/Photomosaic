import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()

filename = filedialog.askopenfilename(parent=root, title='Open file to encrypt')
