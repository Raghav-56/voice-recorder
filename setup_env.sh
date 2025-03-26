#!/bin/bash

# For Ubuntu/Debian-based systems
sudo apt-get update
sudo apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    python3-numpy

# Install Python dependencies
pip install -r requirements.txt

echo "Environment setup complete!"
