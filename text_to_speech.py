# text_to_speech.py
# ---
# Handles converting text strings into spoken audio.

import os

def speak(text):
    """
    Uses the 'espeak' command-line tool to say the given text.
    -s150 sets the speed to 150 words-per-minute.
    """
    print(f"ASSISTANT: {text}")
    os.system(f'espeak "{text}" -s130')