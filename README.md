# Home Assistant

## Summary

Home Assistant is a voice-activated smart home automation system built for Raspberry Pi. It integrates speech recognition, natural language processing, sentiment analysis, and device control to provide an interactive and mood-aware home assistant experience. The system can control various home devices, suggest music based on user mood, tell jokes, fetch weather information, and display status on an LCD screen.

## Table of Contents

- [Project Purpose](#project-purpose)
- [High Level Methodology](#high-level-methodology)
- [Features](#features)
- [Requirements](#requirements)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Requirements](#software-requirements)
- [Libraries](#libraries)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Project Purpose

The Home Assistant project aims to create an intelligent, voice-controlled home automation system that goes beyond simple device control. By incorporating sentiment analysis, the system can adapt its responses and actions based on the user's emotional state, providing a more empathetic and personalized interaction. This project demonstrates the integration of multiple technologies including speech processing, machine learning for sentiment analysis, IoT device control, and real-time data fetching to create a comprehensive smart home solution.

## High Level Methodology

The system operates through a continuous loop:

1. **Initialization**: Calibrates audio input and initializes hardware components (LCD, GPIO pins).

2. **Wake Word Detection**: Listens for the trigger word "assistant" to activate the system.

3. **Command Listening**: Captures user voice commands using speech recognition.

4. **Sentiment Analysis**: Analyzes the emotional tone of the command using natural language processing.

5. **Command Processing**: Interprets the command and performs appropriate actions (device control, information retrieval, etc.).

6. **Response Generation**: Provides audio feedback and updates the LCD display with status information.

7. **Mood-Based Actions**: Adjusts device states (e.g., calming lights) based on detected sentiment.

The methodology emphasizes real-time processing, context awareness, and adaptive responses to create a seamless user experience.

## Features

- **Voice Activation**: Wake word detection for hands-free operation
- **Device Control**: Control of multiple home devices (fan, lights, custom devices) via relay switches
- **Sentiment Analysis**: Mood detection to provide empathetic responses and adaptive actions
- **Music Suggestions**: Personalized music recommendations based on user sentiment
- **Weather Information**: Real-time weather fetching for specified locations
- **Joke Telling**: Entertainment feature with random jokes
- **LCD Display**: Visual feedback showing system status, mood, and actions
- **Mood Indicator**: LED-based visual mood representation (happy, sad, neutral)
- **Context Awareness**: Remembers last mentioned device for follow-up commands
- **Text-to-Speech**: Audio responses for all interactions

## Requirements

### Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- USB Microphone for speech input
- Speaker or audio output device
- I2C LCD Display (16x2 or similar, address 0x27)
- Relay modules for device control (at least 4 channels)
- LEDs for mood indication (Red, Green, Yellow)
- Jumper wires and breadboard for connections
- Power supply for Raspberry Pi and connected devices

### Software Requirements

- Python 3.7+
- Raspbian OS (or compatible Linux distribution)
- Internet connection for weather API and music suggestions

## Libraries

The project uses the following Python libraries:

- `speechrecognition`: For converting speech to text
- `PyAudio`: Audio input/output handling
- `RPi.GPIO`: Raspberry Pi GPIO control for device management
- `nltk`: Natural Language Toolkit for sentiment analysis
- `smbus2`: I2C communication for LCD display
- `pyjokes`: Random joke generation
- `requests`: HTTP requests for weather API calls

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/home_assistant.git
   cd home_assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

3. **Download NLTK data** (required for sentiment analysis):
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

4. **Hardware Setup**:
   - Connect the I2C LCD to the Raspberry Pi's I2C pins
   - Connect relay modules to the specified GPIO pins (see config.py)
   - Connect LEDs to GPIO pins 23, 24, 25 for mood indication
   - Connect microphone and speaker

5. **Configure GPIO**:
   Ensure the GPIO pins in config.py match your hardware setup.

## Usage

1. **Run the main script**:
   ```bash
   python main.py
   ```

2. **Wake the assistant**:
   Say "assistant" to activate the system.

3. **Give commands**:
   - "Turn on fan" / "Turn off fan"
   - "Turn on lights" / "Turn off lights"
   - "Tell me a joke"
   - "What's the weather in [city]?"
   - "Play some music"
   - "I'm feeling happy/sad/stressed"

4. **Exit the system**:
   Say "exit" or "shutdown".

## Configuration

Modify `config.py` to adjust:

- GPIO pin assignments for devices and LEDs
- Wake word (default: "assistant")
- Default location for weather (default: Kolkata)
- Microphone index
- LCD I2C address

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.