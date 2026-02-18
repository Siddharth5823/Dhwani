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
        model = Model(wakeword_models=[config.WAKEWORD_MODEL_PATH], inference_framework="onnx")
        print("✅ Wake Word Ready.")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def detect(audio_data):
    """
    Takes raw audio bytes -> Returns True if wake word detected.
    """
    global model
    if model is None:
        return False

    audio_int16 = np.frombuffer(audio_data, dtype=np.int16)
    
    # Run prediction
    prediction = model.predict(audio_int16)
    
    # Get the score for 'hey_jarvis_v0.1'
    # This will print the confidence (0.0 to 1.0) so you can see it working
    score = list(prediction.values())[0]
    
    if score > 0.2: # Only print if it hears something vaguely like speech
        print(f"DEBUG: Wake Word Score: {score:.4f}", end='\r')
        sys.stdout.write(f"\r[Listening] Confidence: {score:.2f}  ")
        sys.stdout.flush()

    # Return True only if score is high (adjust 0.5 if it's too hard/easy)
    return score > 0.45


'''

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
'''
