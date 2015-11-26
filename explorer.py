import Tkinter
import tkFileDialog

root = Tkinter.Tk()
root.withdraw()

filename = tkFileDialog.askopenfilename(parent=root,title='Open file to encrypt')
