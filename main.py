# main.py
import speech_to_text as stt
import text_to_speech as tts
import sentiment_analysis as sa
import device_control as dc
import lcd_display as lcd
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

    # --- 1. Exit Command (Your "Neel" message is here) ---
    if "exit" in command or "shutdown" in command:
        response = "System is shutting down. Goodbye."
        action_desc = "Goodbye, Neel" # Custom LCD message
        return (False, response, action_desc) 

    # --- 2. Fan Commands ---
    if "turn on fan" in command or "start fan" in command:
        dc.set_device_state('fan', 'on')
        response = "Fan control pin set to low, simulating power ON."
        action_desc = "Fan ON"
            
    elif "turn off fan" in command or "stop fan" in command:
        dc.set_device_state('fan', 'off')
        response = "Fan control pin set to high, simulating power OFF."
        action_desc = "Fan OFF"

    # --- 3. Sentiment-Aware Lights ---
    elif "lights" in command:
        if sentiment == "Stressed ?":
            dc.set_device_state('light', 'on')
            response = "I detect stress. Turning on a soft light to help you relax."
            action_desc = "Calming Light ON"
        elif sentiment == "Happy ?":
            dc.set_device_state('light', 'off')
            response = "You sound cheerful! Adjusting light to a preferred setting."
            action_desc = "Light Control OFF"
        else:
            response = "Light settings remain unchanged."
            action_desc = "Light Neutral"
            
    # --- 4. Sentiment-Aware Music ---
    elif "music" in command:
        if sentiment == "Stressed ?":
            response = "I recommend playing some soothing, calming music now."
            action_desc = "Suggest Calming"
        elif sentiment == "Happy ?":
            response = "Great mood! Initiating cheerful, energetic music."
            action_desc = "Suggest Energetic"
        else:
            response = "I'm not sure what music to play. Your mood is neutral."
            action_desc = "Music Neutral"

    # --- 5. Context-Aware (e.g., "turn it off") ---
    # This is from our new design, you can remove if you don't want it
    elif 'it' in command and last_mentioned_device:
        if 'on' in command:
            response = dc.set_device_state(last_mentioned_device, 'on')
        elif 'off' in command:
            response = dc.set_device_state(last_mentioned_device, 'off')
        action_desc = f"{last_mentioned_device} {command}"
        last_mentioned_device = None # Clear context
            
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