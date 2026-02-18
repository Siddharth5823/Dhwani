#!/bin/bash

MODELS_DIR="models"
mkdir -p "$MODELS_DIR"

echo "---------------------------------"
echo "     DHWANI MODEL DOWNLOADER     "
echo "---------------------------------"

# 1. Vosk Hindi Model
if [ ! -d "$MODELS_DIR/vosk-model-small-hi-0.22" ]; then
    echo "⬇️  Downloading Vosk (Hindi)..."
    wget https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip -P "$MODELS_DIR"
    unzip -o "$MODELS_DIR/vosk-model-small-hi-0.22.zip" -d "$MODELS_DIR"
    rm "$MODELS_DIR/vosk-model-small-hi-0.22.zip"
else
    echo "✅ Vosk Model exists."
fi

# 2. Piper Priyamvada Model (Restored)
if [ ! -f "$MODELS_DIR/hi_IN-priyamvada-medium.onnx" ]; then
    echo "⬇️  Downloading Piper Voice (Priyamvada)..."
    wget -O "$MODELS_DIR/hi_IN-priyamvada-medium.onnx" "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx"
    wget -O "$MODELS_DIR/hi_IN-priyamvada-medium.onnx.json" "https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx.json"
else
    echo "✅ Priyamvada Voice exists."
fi

echo "---------------------------------"
echo "🎉 All Models Ready in '$MODELS_DIR'!"