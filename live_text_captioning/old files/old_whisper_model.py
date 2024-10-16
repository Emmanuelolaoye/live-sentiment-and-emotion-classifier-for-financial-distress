import os
import wave
import pyaudio
from faster_whisper import WhisperModel
import sys
from text_sentiment_analyser import text as text_analyser

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_LENGTH = 6
INPUT = True

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Function for recording an audio fragment
def record_chunk(p, stream, file_path):

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)


    """
    Writes an audio fragment to a file.

    Args:
        p(pyaudio.PyAudio): PyAudio object.
        stream(pyaudio.Stream): PyAudio stream.
        file_path (str): Path to the file where the audio fragment will be recorded.
        chunk_length (int): Length of the audio chunk in seconds.

    Returns:
        None
    """

    for _ in range(0, int(RATE // CHUNK * RECORD_LENGTH)):
        wf.writeframes(stream.read(CHUNK))

    wf.close()

def transcribe_chunk(model, file_path):
    segments, info = model.transcribe(file_path, beam_size=7)
    transcription = ''.join(segment.text for segment in segments)
    return transcription

def transcriber():
    """
        The main function of the program.
    """

    # Choosing a model Whisper
    model = WhisperModel("tiny", device="cpu", compute_type="int16")

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Opening the recording stream
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=INPUT, frames_per_buffer=1024)

    # Initialize an empty string to accumulate transcriptions
    accumulated_transcription = ""

    try:
        while True:
            # Record an audio fragment
            chunk_file = "../audio_chunk/temp_chunk.wav"
            record_chunk(p, stream, chunk_file)

            # We transcribe the audio fragment
            transcription = transcribe_chunk(model, chunk_file)
            text = text_analyser.Text(transcription)
            sentiment = text.get_nltk_sentiment(True)
            text_and_sentiment = transcription + " - " + sentiment

            print(text_and_sentiment)

            # Delete the temporary file
            os.remove(chunk_file)

            # Add a new transcription to the accumulated transcription
            accumulated_transcription += transcription + " "

    except KeyboardInterrupt:
        print("Stopping...")

        # Write the accumulated transcription to a log file
        with open("../text_log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)

    finally:
        print("LOG" + accumulated_transcription)

        # Close the recording stream
        stream.stop_stream()
        stream.close()

        # stop PyAudio
        p.terminate()


if __name__ == "__main__":
    transcriber()