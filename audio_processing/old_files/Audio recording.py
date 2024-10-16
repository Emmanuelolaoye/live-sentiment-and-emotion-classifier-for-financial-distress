import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyaudio

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def speak(text):
    tts = gTTS(text=text)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('[say something]')
        audio = r.listen(source)
        said = ""


        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("error", str(e))
    return said


#speak("hello")
get_audio()

