'''
import os

# Base Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), "models")

# Model Paths
VOSK_MODEL_PATH = os.path.join(MODELS_DIR, "vosk-model-small-hi-0.22")
TTS_MODEL = os.path.join(MODELS_DIR, "hi_IN-priyamvada-medium.onnx")
PIPER_PATH = os.path.join(MODELS_DIR, "piper", "piper")

# Audio Settings
SAMPLE_RATE = 16000
WAKE_WORD = "jarvis"  # We will detect this inside the speech
'''

import os

# --- PATHS ---
# src/ is the base, so we go up one level to find 'models'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

# --- MODEL FILES ---
# 1. Wake Word (OpenWakeWord)
# Ensure your script saved it as 'hey_jarvis_v0.1.onnx' or 'hey_jarvis.onnx'
WAKEWORD_MODEL_PATH = os.path.join(MODELS_DIR, "hey_jarvis_v0.1.onnx") 

# 2. Speech-to-Text (Vosk)
# Ensure your script extracted it to this folder name
VOSK_MODEL_PATH = os.path.join(MODELS_DIR, "vosk-model-small-hi-0.22")

# 3. Text-to-Speech (Piper)
PIPER_PATH = os.path.join(MODELS_DIR, "piper", "piper")
TTS_MODEL = os.path.join(MODELS_DIR, "hi_IN-priyamvada-medium.onnx")

# --- AUDIO SETTINGS ---
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # Optimized for OpenWakeWord
