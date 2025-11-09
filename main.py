# main.py
import speech_to_text as stt
import text_to_speech as tts
import sentiment_analysis as sa
import device_control as dc
import lcd_display as lcd
import telljokes as jk
import weather_fetcher as wf
import config as Config
import mood_indicator as mi
import music_suggester as ms
import time

# This variable will store the last mentioned device for context
last_mentioned_device = None

def process_command(command, sentiment):
    """
    Analyzes command and sentiment, returns (should_continue, response_text, action_desc)
    This logic is now merged from your old 'process_command'.
    """
    global last_mentioned_device
    response = f"You seem {sentiment}. I'm ready for a command." # Default
    action_desc = f"Mood: {sentiment}"
    mi.display_mood(sentiment)

    # --- 1. Exit Command (Your "Neel" message is here) ---
    if "exit" in command or "shutdown" in command:
        response = "System is shutting down. Goodbye."
        action_desc = "Goodbye, Neel" # Custom LCD message
        return (False, response, action_desc) 

    # --- 2. Fan Commands ---
    if "turn on fan" in command or "start fan" in command or "activate fan" in command or "switch on fan" in command or "fan on" in command or "fan start" in command or "turn the fan on" in command:
        dc.set_device_state('fan', 'on')
        response = "Sure,  Fan control pin set to low, simulating power ON."
        action_desc = "Fan ON"
            
    elif "turn off fan" in command or "stop fan" in command or "deactivate fan" in command or "switch off fan" in command or "fan off" in command or "fan stop" in command or "turn the fan off" in command:
        dc.set_device_state('fan', 'off')
        response = "Sure,  Fan control pin set to high, simulating power off."
        action_desc = "Fan OFF"
    # --- Device Commands ---
    elif "turn on device 2" in command or "start device 2" in command or "activate device 2" in command or "switch on device 2" in command or "device 2 on" in command or "device 2 start" in command or "turn the device 2 on" in command:
        dc.set_device_state('device 2', 'on')
        response = "Sure, Device 2 control pin set to low, simulating power ON."
        action_desc = "Device 2 ON"
            
    elif "turn off device 2" in command or "stop device 2" in command or "deactivate device 2" in command or "switch off device 2" in command or "device 2 off" in command or "device 2 stop" in command or "turn the device 2 off" in command:
        dc.set_device_state('device 2', 'off')
        response = "Sure, Device 2 control pin set to high, simulating power off."
        action_desc = "Device 2 OFF"
    elif "turn on device 3" in command or "start device 3" in command or "activate device 3" in command or "switch on device 3" in command or "device 3 on" in command or "device 3 start" in command or "turn the device 3 on" in command:
        dc.set_device_state('device 3', 'on')
        response = "Sure, Device 3 control pin set to low, simulating power ON."
        action_desc = "Device 3 ON"
            
    elif "turn off device 3" in command or "stop device 3" in command or "deactivate device 3" in command or "switch off device 3" in command or "device 3 off" in command or "device 3 stop" in command or "turn the device 3 off" in command:
        dc.set_device_state('device 3', 'off')
        response = "Sure, Device 3 control pin set to high, simulating power off."
        action_desc = "Device 3 OFF"

            
    # --- 4. Sentiment-Aware Music ---
    elif "music" in command or "play a song" in command:
        # Call the new music suggester function
        response = ms.get_track_suggestion(sentiment)
        action_desc = "Music Suggestion"
    

    # --- 5. Context-Aware (e.g., "turn it off") ---
    # This is from our new design, you can remove if you don't want it
    elif 'it' in command and last_mentioned_device:
        if 'on' in command:
            response = dc.set_device_state(last_mentioned_device, 'on')
        elif 'off' in command:
            response = dc.set_device_state(last_mentioned_device, 'off')
        action_desc = f"{last_mentioned_device} {command}"
        last_mentioned_device = None # Clear context
    
    # --- Jokes ---
    elif "joke" in command:
        joke = jk.tell_joke()
        response = joke
        action_desc = "Told a joke"

    # --- NEW: Weather Command Logic ---
    elif "weather" in command or "forecast" in command:
        # Simple extraction: look for "in [city]" or "for [city]"
        
        # Try to find a specific city mentioned (e.g., "what is the weather in Paris")
        city = None
        
        # This is a very simple way to grab the city name
        if 'in' in command:
            parts = command.split('in')
            if len(parts) > 1:
                city = parts[1].strip().split()[0] # Grab the first word after 'in'
        elif 'for' in command:
            parts = command.split('for')
            if len(parts) > 1:
                city = parts[1].strip().split()[0]
                
        # Handle the special case where the user might say the trigger word again
        if city == "assistant" or city == "Neel":
            city = None 

        weather_response = wf.get_current_weather(city)
        response = weather_response
        action_desc = f"Weather in {city if city else "Kolkata"}"           
    
    elif "feeling" in command or "mood" in command:
        if "sad" in command or "unhappy" in command or "not good" in command or "depressed" in command or "down" in command or "angry" in command or "frustrated" in command or "upset" in command or "mad" in command:
            sentiment = "stressed"
            dc.set_device_state('calming light', 'off')
            response = "I'm sorry to hear that you're feeling stressed. I've turned on the calming light to help you relax.   You can also listen to some soothing music if you'd like."
            action_desc = "Calming Light ON"
        elif "happy" in command or "good" in command or "great" in command or "fantastic" in command or "joyful" in command or "excited" in command or "cheerful" in command or "content" in command or "pleased" in command:
            sentiment = "happy"
            dc.set_device_state('calming light', 'on')
            response = "That's wonderful to hear! I've turned off the calming light to match your upbeat mood. Enjoy your day!"
            action_desc = "Calming Light OFF"
            
    # -- for Lights --
    elif "turn on lights" in command or "start lights" in command or "activate lights" in command or "switch on light" in command or "lights on" in command or "lights start" in command or "turn the lights on" in command:
        dc.set_device_state('lights', 'off')
        response = "Sure, Lights Turned ON."
        action_desc = "Lights ON"
            
    elif "turn off lights" in command or "stop lights" in command or "deactivate lights" in command or "switch off lights" in command or "lights off" in command or "lights stop" in command or "turn the lights off" in command:
        dc.set_device_state('light', 'on')
        response = "Sure, Device 2 control pin set to high, simulating power off."
        action_desc = "Device 2 OFF"
    return (True, response, action_desc) 


def main():
    # --- 1. Initialization ---
    lcd.init()
    tts.speak("System initializing. Please remain silent for audio calibration.")
    lcd.display_message("Calibrating...", "Please be quiet...")
    
    stt.calibrate_noise()
    
    tts.speak("Calibration complete. System ready.")
    lcd.display_message("Assistant Ready", "Awaiting call...")
    
    try:
        while True:
            # --- 2. Wait for Wake Word ---
            if stt.listen_for_wake_word():
                
                # --- 3. Listen for Command ---
                tts.speak("Yes?")
                lcd.display_message("Yes?", "Listening...")
                command = stt.listen_for_command()
                
                if command:
                    # --- 4. Process ---
                    sentiment = sa.get_sentiment(command)
                    (should_run, response, action) = process_command(command, sentiment)
                    
                    # --- 5. Feedback ---
                    tts.speak(response)
                    # Use the special "Goodbye, Neel" message on line 2 if shutting down
                    if not should_run:
                        lcd.display_message("System Shutting", action)
                    else:
                        lcd.display_message(f"Mood: {sentiment}", f"Action: {action}")
                    
                    if not should_run:
                        break # Exit loop
                else:
                    # Handle no command heard
                    tts.speak("Sorry, I didn't catch that.")
                    lcd.display_message("Error:", "No command heard.")
                
                time.sleep(2) # Pause before resetting LCD
                lcd.display_message("Assistant Ready", "Awaiting call...")
                
    except KeyboardInterrupt:
        print("\nShutdown signal received.")
    finally:
        dc.cleanup()
        lcd.clear()
        if 'action' in locals() and action == "Goodbye, Neel":
            pass # Don't say goodbye twice
        else:
            tts.speak("Shutting down. Goodbye.")
        print("Assistant offline.")

if __name__ == "__main__":
    main()