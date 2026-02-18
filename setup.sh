#!/bin/bash

echo "🚀 STARTING DHWANI SETUP..."

# 1. Install System Libraries
echo "🔧 Installing System Libraries..."
sudo apt update
sudo apt install -y python3-pip python3-venv portaudio19-dev libasound2-dev libsndfile1 espeak-ng git wget unzip swig

# 2. Set up Python Environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Virtual Environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Install Python Libraries (Removing OWW/ONNX-Runtime bloat)
echo "📦 Installing Python Dependencies..."
pip install --upgrade pip
# We keep Piper and Vosk, but remove openwakeword
pip install pocketsphinx vosk pyaudio numpy

# 4. Run Model Downloader
chmod +x download_models.sh
./download_models.sh

echo "✅ SETUP COMPLETE!"