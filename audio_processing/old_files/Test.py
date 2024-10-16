# importing all files from tkinter
import SystemSpeakerRecorder
import RecordingManager as recorder

from tkinter import *
from tkmacosx import *




"""

While True:
    try:
        recording_function()

    except KeyboardInterrupt:
        save_function() #record to a file
    except: 
        #generic error processing
        
"""

def recordBttn():
    pass


def record():
    startRecodrding = recorder.record()
    pass


# import only asksaveasfile from filedialog
# which is used to save file in any extension
from tkinter.filedialog import asksaveasfile

root = Tk()
root.geometry('500x500')


# function to call when user press
# the save button, a filedialog will
# open and ask to save file

def save():
    files = [('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]


    print(asksaveasfile(filetypes=files, defaultextension=files).name)


buttonFrame = Frame(root, bg='red')
textFrame = Frame(root, bg='green')

buttonFrame.pack(side=LEFT)
textFrame.pack(side=RIGHT)








savebtn = Button(buttonFrame, text='Save', bg='#3E4149', command=lambda: save())
recordbtn = Button(buttonFrame, text='record', command=lambda: recordBttn())
pausebtn = Button(buttonFrame, text='pause', command=lambda: recordBttn())
stopbtn = Button(buttonFrame, text='stop', command=lambda: recordBttn())

recordbtn.pack(side=TOP, pady=5)
pausebtn.pack(side=TOP, pady=5)
stopbtn.pack(side=TOP, pady=5)
savebtn.pack(side=TOP, pady=5)

root.mainloop()
