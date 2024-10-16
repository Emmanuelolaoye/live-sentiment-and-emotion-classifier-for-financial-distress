import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyttsx3

for index , name in enumerate(sr.Microphone.list_microphone_names()):
    print("name \"{1}\"found for 'mic(device_index={0}')".format(index, name))


def speak2txt(cmd):
    engine = pyttsx3.init()
    engine.say(cmd)
    engine.runAndWait()




while(1):


    try:

        r = sr.Recognizer()
        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source)

            print("say something")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()

            print(text)

    except sr.RequestError as e:
        print('cant request results; {0}'.format(e))

    except sr.UnknownValueError as e:
        print("unknown value")