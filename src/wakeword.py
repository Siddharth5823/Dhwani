import openwakeword
from openwakeword.model import Model
import config
import os
import numpy as np

# Global variable to hold the model
model = None

def load_model():
    """Loads the model into memory. Returns True if successful."""
    global model
    print(f"⚡ Loading Wake Word: {os.path.basename(config.WAKEWORD_MODEL_PATH)}...")
    
    if not os.path.exists(config.WAKEWORD_MODEL_PATH):
        print(f"❌ Error: Model not found at {config.WAKEWORD_MODEL_PATH}")
        print("👉 Did you run './download_models.sh'?")
        return False

    try:
        # Load the specific model path
        model = Model(wakeword_models=[config.WAKEWORD_MODEL_PATH])
        print("✅ Wake Word Ready.")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def detect(audio_chunk_bytes):
    """
    Takes raw audio bytes -> Returns True if wake word detected.
    """
    global model
    if model is None:
        return False

    # Convert bytes to numpy array (int16)
    audio_int16 = np.frombuffer(audio_chunk_bytes, dtype=np.int16)
    
    # Feed to model
    prediction = model.predict(audio_int16)
    
    # Check score (Threshold 0.5 is standard)
    # The key name depends on the model file. Usually it's the filename without extension.
    # We use list(prediction.keys())[0] to be safe.
    model_name = list(prediction.keys())[0]
    if prediction[model_name] > 0.5:
        return True
    
    return False
