import pyjokes
import text_to_speech as tts

def tell_joke():
    """Fetches a random joke and uses TTS to tell it."""
    joke = pyjokes.get_joke()
    print(f"JOKE: {joke}")
    tts.speak(joke)


