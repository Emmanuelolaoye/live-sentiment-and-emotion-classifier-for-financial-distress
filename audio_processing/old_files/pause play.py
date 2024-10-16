import sys
import tkinter as tk
import pyaudio
import wave
from tkinter.filedialog import asksaveasfile


class RecAUD:


    def __init__(self, chunk=1024, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):
        # Start Tkinter and set Title
        self.main = tk.Tk()
        self.main.geometry('500x300')
        self.main.title('Record')

        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = 1 if sys.platform == 'darwin' else 2
        self.RATE = rate
        self.p = py
        self.frames = []
        self.stream = None
        self.is_recording = False

        # Set Frames
        self.buttons = tk.Frame(self.main, padx=20, pady=20)
        self.buttons.pack(fill=tk.BOTH)

        # Button Definitions
        self.strt_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Start Recording',
                                  command=self.start_record)
        self.strt_rec.grid(row=0, column=0, padx=50, pady=5)

        self.stop_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Stop Recording', command=self.stop)
        self.stop_rec.grid(row=1, column=0, padx=50, pady=5)

        self.pause_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Pause', command=self.pause)
        self.pause_rec.grid(row=0, column=1, padx=50, pady=5)

        self.resume_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Resume', command=self.resume)
        self.resume_rec.grid(row=1, column=1, padx=50, pady=5)

        tk.mainloop()

    def start_record(self):
        self.is_recording = True
        self.frames = []
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)
        while self.is_recording:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            self.frames.append(data)
            print("* recording")
            self.main.update()

    def stop(self):
        print("* stopped")
        self.is_recording = False
        self.stream.close()
        wf = wave.open(self.save(), 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def pause(self):
        self.is_recording = False
        print("* paused")

    def resume(self):
        self.is_recording = True
        self.start_record()
        print("* resumed")

    def save(self):
        files = [('Sound Recording', '*.wav'), ('All Files', '*.*'), ('Python Files', '*.py')]

        return asksaveasfile(filetypes=files, defaultextension=".wav").name


# Create an object of the RecAUD class to begin the program.
guiAUD = RecAUD()
