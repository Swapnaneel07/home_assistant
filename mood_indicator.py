# mood_indicator.py

import RPi.GPIO as GPIO
from config import Config
import time

def all_off():
    """Turns off all mood indicator LEDs."""
    GPIO.output(Config.GREEN_LED, GPIO.LOW)
    GPIO.output(Config.YELLOW_LED, GPIO.LOW)
    GPIO.output(Config.RED_LED, GPIO.LOW)

def display_mood(sentiment):
    """
    Lights up the appropriate LED based on the sentiment.
    
    Args:
        sentiment (str): The classification result from sentiment analysis 
                         (e.g., "Happy ?", "Stressed ?", "Neutral").
    """
    
    all_off() # Always start by turning all lights off

    if "Happy" in sentiment or "Positive" in sentiment:
        # Green LED for Positive
        GPIO.output(Config.GREEN_LED, GPIO.HIGH)
        print("Mood LED: Green (Happy) ON")
        
    elif "Stressed" in sentiment or "Negative" in sentiment:
        # Red LED for Negative
        GPIO.output(Config.RED_LED, GPIO.HIGH)
        print("Mood LED: Red (Stressed) ON")
        
    else:
        # Yellow LED for Neutral or Unknown
        GPIO.output(Config.YELLOW_LED, GPIO.HIGH)
        print("Mood LED: Yellow (Neutral) ON")

    # Keep the LED on for a short period to be visible
    # The next call to display_mood will automatically turn this one off
    # when all_off() is called.