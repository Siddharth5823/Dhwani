#!/bin/bash

# Define Directory
MODELS_DIR="models"
mkdir -p "$MODELS_DIR"

echo "---------------------------------"
echo "     DHWANI MODEL DOWNLOADER     "
echo "---------------------------------"

# 1. Download VOSK (Hearing) - Hindi
if [ ! -d "$MODELS_DIR/vosk-model-small-hi-0.22" ]; then
    echo "⬇️  Downloading Vosk (Hindi)..."
    wget https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip -P "$MODELS_DIR"
    echo "📦 Extracting Vosk..."
    unzip -o "$MODELS_DIR/vosk-model-small-hi-0.22.zip" -d "$MODELS_DIR"
    rm "$MODELS_DIR/vosk-model-small-hi-0.22.zip"
else
    echo "✅ Vosk Model already exists."
fi

# 2. Download PIPER (Voice) - Priyamvada
if [ ! -f "$MODELS_DIR/hi_IN-priyamvada-medium.onnx" ]; then
    echo "⬇️  Downloading Piper Voice (Priyamvada)..."
    wget -O "$MODELS_DIR/hi_IN-priyamvada-medium.onnx" "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/en_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx"
    wget -O "$MODELS_DIR/hi_IN-priyamvada-medium.onnx.json" "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/en_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx.json"
else
    echo "✅ Piper Voice already exists."
fi
# 3. Download OPENWAKEWORD (Trigger) - Hey Jarvis
if [ ! -f "$MODELS_DIR/hey_jarvis_v0.1.onnx" ]; then
    echo "⬇️  Downloading Wake Word (Hey Jarvis)..."
    # We navigate into the folder, let Python download it, then come back
    cd "$MODELS_DIR"
    python3 -c "import openwakeword.utils; openwakeword.utils.download_models(['hey_jarvis_v0.1'])"
    cd ..
else
    echo "✅ Wake Word Model already exists."
fi

# 3. Download OPENWAKEWORD (Trigger) - Hey Jarvis
#if [ ! -f "$MODELS_DIR/hey_jarvis_v0.1.onnx" ]; then
 #   echo "⬇️  Downloading Wake Word (Hey Jarvis)..."
  #  # UPDATED LINK (HuggingFace)
   # wget -O "$MODELS_DIR/hey_jarvis_v0.1.onnx" "https://huggingface.co/dscripka/openWakeWord/resolve/main/hey_jarvis_v0.1.onnx"
#else
 #   echo "✅ Wake Word Model already exists."
#fi

echo "---------------------------------"
echo "🎉 All Models Ready in '$MODELS_DIR'!"
