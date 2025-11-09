# device_control.py
import RPi.GPIO as GPIO
import mood_indicator as mi
from config import Config

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up pins with default state as OFF
GPIO.setup(Config.RELAY_PIN_FAN, GPIO.OUT, initial=Config.DEVICE_OFF)
GPIO.setup(Config.RELAY_PIN_DEVICE_2, GPIO.OUT, initial=Config.DEVICE_OFF)
GPIO.setup(Config.RELAY_PIN_DEVICE_3, GPIO.OUT, initial=Config.DEVICE_OFF)
GPIO.setup(Config.GREEN_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Config.YELLOW_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Config.RED_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Config.GPIO_LIGHT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Config.GPIO_CALMING_LIGHT, GPIO.OUT, initial=GPIO.LOW)

def set_device_state(device_name, state):
    """
    Controls a device ('fan' or 'light') using active-low logic.
    """
    pin = None
    output_state = None
    
    if device_name == 'fan':
        pin = Config.RELAY_PIN_FAN
    elif device_name == 'device 2':
        pin = Config.RELAY_PIN_DEVICE_2
    elif device_name == 'device 3':
        pin = Config.RELAY_PIN_DEVICE_3
    elif device_name == 'lights':
        pin = Config.GPIO_LIGHT
    elif device_name == 'calming light':
        pin = Config.GPIO_CALMING_LIGHT
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
    GPIO.output(Config.RELAY_PIN_FAN, Config.DEVICE_OFF) # Turn off fan
    GPIO.output(Config.GPIO_LIGHT, Config.DEVICE_ON)  # Turn off lights
    GPIO.output(Config.RELAY_PIN_DEVICE_2, Config.DEVICE_OFF) 
    GPIO.output(Config.RELAY_PIN_DEVICE_3, Config.DEVICE_OFF)
    mi.all_off()  # Turn off mood indicator LEDs
    GPIO.cleanup()