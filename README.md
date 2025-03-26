# voice-recorder
Voice recorder app





# Voice Recorder Project

## Introduction
This project is a simple voice recorder application built in Python. It allows users to record their voice, store the recordings in a dedicated folder, and play them back. The application is designed to be minimal and easy to use, making it suitable for beginners.

## Project Structure
```
voice-recorder
├── src
│   ├── voice_recorder.py   # Main script for the command-line interface
│   ├── audio_handler.py     # Handles audio recording and playback
│   └── utils.py            # Utility functions for file management
├── recordings               # Directory to store recorded audio files
│   └── .gitkeep             # Keeps the recordings directory in version control
├── requirements.txt         # Lists required Python libraries
├── README.md                # Project documentation
└── .gitignore               # Specifies files to ignore in version control
```

## Installation
To run this project, you need to install the required Python libraries. You can do this using pip. Run the following command in your terminal:

```
pip install -r requirements.txt
```

## Usage
1. Navigate to the project directory:
   ```
   cd voice-recorder
   ```

2. Run the application:
   ```
   python src/voice_recorder.py
   ```

3. Follow the command-line interface prompts to:
   - Start recording
   - Stop recording and save the file
   - List available recordings
   - Play a selected recording
   - Exit the application

## Dependencies
This project requires the following Python libraries:
- pyaudio or sounddevice (for audio recording and playback)

## Contributing
Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.

## License
This project is open-source and available under the MIT License.
