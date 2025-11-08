# device_control.py
import RPi.GPIO as GPIO
from config import Config

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up pins with default state as OFF
GPIO.setup(Config.RELAY_PIN_FAN, GPIO.OUT, initial=Config.DEVICE_OFF)
GPIO.setup(Config.RELAY_PIN_LIGHT, GPIO.OUT, initial=Config.DEVICE_OFF)
GPIO.setup(Config.RELAY_PIN_CALM_LIGHT, GPIO.OUT, initial=Config.DEVICE_OFF)
GPIO.setup(Config.GREEN_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Config.YELLOW_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Config.RED_LED, GPIO.OUT, initial=GPIO.LOW)

def set_device_state(device_name, state):
    """
    Controls a device ('fan' or 'light') using active-low logic.
    """
    pin = None
    output_state = None
    
    if device_name == 'fan':
        pin = Config.RELAY_PIN_FAN
    elif device_name == 'light':
        pin = Config.RELAY_PIN_LIGHT
    elif device_name == 'claming_lights':
        pin = Config.RELAY_PIN_CALM_LIGHT
    else:
        return f"Unknown device: {device_name}"
        
    if state == 'on':
        output_state = Config.DEVICE_ON
    elif state == 'off':
        output_state = Config.DEVICE_OFF
    else:
        return f"Unknown state: {state}"
        
    GPIO.output(pin, output_state)
    
    # Return a simple description for the main loop to speak
    return f"{device_name.capitalize()} turned {state}."

def cleanup():
    """Cleans up GPIO pins on exit."""
    print("Cleaning up GPIO pins...")
    GPIO.output(Config.RELAY_PIN_FAN, Config.DEVICE_OFF)
    GPIO.output(Config.RELAY_PIN_LIGHT, Config.DEVICE_OFF)
    GPIO.cleanup()