import torch
import soundfile as sf
import numpy as np
import librosa
from TTS.api import TTS
import IPython.display as ipd
import subprocess
import os

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load an offline TTS model
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)

def generate_speech(text, output_path="output.wav"):
    """ Generate speech from text and save it to a WAV file """
    print("Generating speech...")
    tts.tts_to_file(text=text, file_path=output_path)
    print(f"Audio saved as {output_path}")

    # Increase volume
    louder_path = "output_louder.wav"
    increase_volume(output_path, louder_path)

    # Play final audio in Google Colab
    return play_audio(louder_path)

def play_audio(file_path):
    """ Play audio in Google Colab using IPython.display.Audio """
    try:
        return ipd.Audio(file_path, autoplay=True)
    except Exception as e:
        print(f"Error playing audio: {e}")

def increase_volume(input_file, output_file, gain=5.0):
    """ Increase volume of the WAV file """
    try:
        audio, sr = librosa.load(input_file, sr=None)
        audio = np.clip(audio * gain, -1.0, 1.0)  # Prevent clipping
        sf.write(output_file, audio, sr)
        print(f"Volume increased: {output_file}")
    except Exception as e:
        print(f"Error increasing volume: {e}")

# Get user input and generate speech
user_text = input("Enter text to generate speech: ")
audio_output = generate_speech(user_text)

# Display & play the audio in Colab
audio_output
