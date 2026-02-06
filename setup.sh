#!/bin/bash
echo "Setting up the Environment..."
sudo apt update && sudo apt install -y python3-pyaudio libasound2-dev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Setup Complete!"
