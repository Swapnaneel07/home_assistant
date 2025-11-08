# config.py
import RPi.GPIO as GPIO

class Config:
    # GPIO Pins
    RELAY_PIN_FAN = 17      # GPIO 17 (Fan/Device 1)
    RELAY_PIN_LIGHT = 27    # GPIO 27 (Light/Device 2)
    RELAY_PIN_CALM_LIGHT = 22 # GPIO 22 (Calm Light/Device 3)

    # Relay Logic (Active-Low from your code)
    DEVICE_ON = GPIO.LOW    # LOW = ON
    DEVICE_OFF = GPIO.HIGH  # HIGH = OFF
    
    # Audio/Speech
    MIC_INDEX = 1           # Your specific mic index
    TRIGGER_WORD = "pi"
    
    # I2C LCD (Matches your old main.py)
    LCD_ADDRESS = 0x27      
    PI_REVISION = 2

    DEFAULT_LATITUDE = 22.56750
    DEFAULT_LONGITUDE = 88.37000
    DEFAULT_LOCATION_NAME = "Kolkata"
    
    GREEN_LED = 25
    RED_LED = 23
    YELLOW_LED = 24

