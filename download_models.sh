#!/bin/bash

# Define directories
MODEL_DIR="models"
mkdir -p $MODEL_DIR

echo "Downloading Vosk Hindi Model (ASR)..."
wget https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip -P $MODEL_DIR
echo "Unzipping Vosk Model..."
unzip $MODEL_DIR/vosk-model-small-hi-0.22.zip -d $MODEL_DIR
mv $MODEL_DIR/vosk-model-small-hi-0.22 $MODEL_DIR/vosk-model
rm $MODEL_DIR/vosk-model-small-hi-0.22.zip

echo "Downloading Piper TTS Binary (arm64)..."
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz -P $MODEL_DIR
tar -xvf $MODEL_DIR/piper_linux_aarch64.tar.gz -C $MODEL_DIR
rm $MODEL_DIR/piper_linux_aarch64.tar.gz

echo "Downloading Hindi Voice (ONNX)..."
wget -O models/hi_IN-priyamvada-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx
wget -O models/hi_IN-priyamvada-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx.json

#echo Downloading Hindi Voice (ONNX)...
#wget https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/en_IN/alma/medium/hi_IN-alma-medium.onnx -P $MODEL_DIR
#wget https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/en_IN/alma/medium/hi_IN-alma-medium.onnx.json -P $MODEL_DIR

echo "------------------------------------------------"
echo "All models downloaded successfully to '$MODEL_DIR/'"
echo "You are ready to run the project!"
