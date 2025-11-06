# speech_to_text.py
import speech_recognition as sr
from config import Config

recognizer = sr.Recognizer()

# Use the specific microphone index from Config
try:
    microphone = sr.Microphone(device_index=Config.MIC_INDEX)
except AssertionError:
    print(f"Error: Microphone with index {Config.MIC_INDEX} not found.")
    print("Using default microphone.")
    microphone = sr.Microphone()

def calibrate_noise():
    """Calibrates for ambient noise."""
    with microphone as source:
        print("Calibrating for ambient noise, please wait...")
        # Use duration from your main.py
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("Calibration complete.")

def listen_for_wake_word():
    """Listens continuously for the wake word."""
    print(f"\nListening for wake word ('{Config.TRIGGER_WORD}')...")
    with microphone as source:
        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio).lower()
                
                if Config.TRIGGER_WORD in text:
                    print("Wake word detected!")
                    return True
            except sr.UnknownValueError:
                pass 
            except sr.RequestError as e:
                print(f"Speech recognition service error; {e}")
                
def listen_for_command():
    """Listens for a single command after the wake word."""
    print("Listening for command...")
    with microphone as source:
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio).lower()
            print(f"USER: {text}")
            return text
        except sr.UnknownValueError:
            return None 
        except sr.RequestError as e:
            print(f"Speech recognition service error; {e}")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None