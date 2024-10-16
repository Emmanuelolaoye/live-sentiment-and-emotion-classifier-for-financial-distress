import moviepy.editor as mp
import speech_recognition as sr


# Load the video
video = mp.VideoFileClip(r"M:\00 School-Work\DIssertation\example video.mp4")

# Extract the audio from the video
audio_file = video.audio
audio_file.write_audiofile("example video.wav")

# Initialize recognizer
r = sr.Recognizer()
print(r)

# Load the audio file
with sr.AudioFile("example video.wav") as source:
    data = r.record(source)

#(data)

# Convert speech to text
text = r.recognize_google(data, key="AIzaSyDRdSN1VaRW27HxA68rZW5FesS2qoPD8",language = 'en-US', show_all=True)

# Print the text
print("\nThe resultant text from video is: \n")
print(text)