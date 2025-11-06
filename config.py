# config.py
import RPi.GPIO as GPIO

class Config:
    # GPIO Pins
    RELAY_PIN_FAN = 17      # GPIO 17 (Fan/Device 1)
    RELAY_PIN_LIGHT = 27    # GPIO 27 (Light/Device 2)
    
    # Relay Logic (Active-Low from your code)
    DEVICE_ON = GPIO.LOW    # LOW = ON
    DEVICE_OFF = GPIO.HIGH  # HIGH = OFF
    
    # Audio/Speech
    MIC_INDEX = 1           # Your specific mic index
    TRIGGER_WORD = "assistant"
    
    # I2C LCD (Matches your old main.py)
    LCD_ADDRESS = 0x27      
    PI_REVISION = 2