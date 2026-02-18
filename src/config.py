import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

WAKEWORD_MODEL_PATH = os.path.join(MODELS_DIR, "hey_jarvis_v0.1.onnx") 

VOSK_MODEL_PATH = os.path.join(MODELS_DIR, "vosk-model-small-hi-0.22")

PIPER_PATH = os.path.join(MODELS_DIR, "piper", "piper")
TTS_MODEL = os.path.join(MODELS_DIR, "hi_IN-priyamvada-medium.onnx")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280 
