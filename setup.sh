#!/bin/bash

echo "🚀 STARTING DHWANI SETUP..."

# 1. Update System & Install Dependencies
echo "🔧 Installing System Libraries..."
sudo apt update
sudo apt install -y python3-pip python3-venv portaudio19-dev libsndfile1 espeak-ng git wget unzip

# 2. Set up Python Environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Virtual Environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# 3. Install Python Libraries
echo "📦 Installing Python Dependencies..."
pip install --upgrade pip
# Install openwakeword specifically + other requirements
pip install openwakeword onnxruntime sounddevice vosk numpy

# 4. Run the Model Downloader [THIS IS THE ONE-CLICK MAGIC]
echo "📥 Checking Models..."
chmod +x download_models.sh
./download_models.sh

echo "---------------------------------------------"
echo "✅ SETUP COMPLETE!"
echo "👉 To start: 'source venv/bin/activate' then 'python src/main.py'"
echo "---------------------------------------------"
