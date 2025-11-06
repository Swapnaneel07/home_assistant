# lcd_display.py
# ---
# Manages the I2C LCD display using your specific 'LCD.py' library.

from config import Config
from LCD import LCD  # Using your confirmed working library
import time

# Initialize the LCD object
lcd = None

def init():
    """Initializes the LCD display."""
    global lcd
    try:
        lcd = LCD(pi_rev=Config.PI_REVISION, i2c_addr=Config.LCD_ADDRESS, backlight=True)
        print("LCD Display initialized.")
        lcd.clear()
    except Exception as e:
        print(f"Error initializing LCD: {e}")
        print("LCD functions will be disabled.")
        lcd = None

def display_message(line1="", line2=""):
    """
    Displays a two-line message on the LCD.
    Clears the screen first.
    """
    if not lcd:
        return # Do nothing if LCD failed to init
        
    try:
        lcd.clear()
        lcd.message(line1[:16], 1) # Use .message() as in your old code
        lcd.message(line2[:16], 2) # Truncate to 16 chars
    except Exception as e:
        print(f"Error writing to LCD: {e}")

def clear():
    """Clears the LCD screen."""
    if not lcd:
        return
        
    try:
        lcd.clear()
    except Exception as e:
        print(f"Error clearing LCD: {e}")