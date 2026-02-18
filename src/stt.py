'''
import json
import queue
import time

# ... (existing imports and model loading)

def listen_from_queue(audio_queue, timeout=5):
    """
    Listens to the EXISTING audio queue for a command.
    Stops if silence is detected or timeout reached.
    """
    print("   (STT Listening...)")
    
    # Reset the recognizer to clear old buffers
    rec.Reset()
    
    start_time = time.time()
    
    while True:
        # 1. CHECK TIMEOUT
        if time.time() - start_time > timeout:
            print("   (STT Timeout)")
            # Force return whatever is in the buffer (e.g. partial sentence)
            final_res = json.loads(rec.FinalResult())
            return final_res.get('text', '').lower()

        try:
            # 2. GET AUDIO
            # Use a short timeout on the queue get so we can check the loop timer
            data = audio_queue.get(timeout=0.2) 
            
            # 3. FEED TO VOSK
            if rec.AcceptWaveform(data):
                # User stopped speaking (Sentence Complete)
                result = json.loads(rec.Result())
                text = result.get('text', '')
                if text:
                    return text.lower()
            else:
                # User is still speaking (or silence)
                # Reset timer if we detect *partial* speech (Optional but good)
                partial = json.loads(rec.PartialResult())
                if partial.get('partial', ''):
                    start_time = time.time() # Extend timeout if user is talking

        except queue.Empty:
            continue


import sounddevice as sd
import json
import sys
import os
from vosk import Model, KaldiRecognizer
import config

# Initialize Model ONCE
print("⚡ Loading Vosk...")
if not os.path.exists(config.VOSK_MODEL_PATH):
    print("❌ Model not found!")
    sys.exit(1)

model = Model(config.VOSK_MODEL_PATH)

def listen():
    """
    Opens Mic -> Listens for ONE command -> Closes Mic -> Returns Text
    """
    # Create a recognizer for this specific listening session
    rec = KaldiRecognizer(model, config.SAMPLE_RATE)
    
    print("   (STT Listening...)")
    
    # Open a BLOCKING stream (Simpler than callbacks)
    with sd.RawInputStream(samplerate=config.SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1) as stream:
        while True:
            # READ audio directly (No Queue)
            data, overflow = stream.read(4000)
            
            if rec.AcceptWaveform(bytes(data)):
                result = json.loads(rec.Result())
                text = result.get('text', '')
                if text:
                    return text.lower()


import sounddevice as sd
import json
import sys
import os
from vosk import Model, KaldiRecognizer
import config

# We leave the model variable empty at first
model = None

def listen():
    global model
    
    # ONLY load the model if it hasn't been loaded yet
    if model is None:
        print("⚡ Loading Vosk (Ears) for the first time...")
        model = Model(config.VOSK_MODEL_PATH)
        print("✅ Vosk Ready.")

    rec = KaldiRecognizer(model, config.SAMPLE_RATE)
    
    print("   (Listening for command...)")
    with sd.RawInputStream(samplerate=config.SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, device=1) as stream:
        while True:
            data, overflow = stream.read(4000)
            if rec.AcceptWaveform(bytes(data)):
                result = json.loads(rec.Result())
                return result.get('text', '').lower()
'''

import sounddevice as sd
import json
import os
import sys
from vosk import Model, KaldiRecognizer
import config

# Global variable to keep the model in memory once loaded
_vosk_model = None

def load_model():
    """Loads the model into RAM only when called."""
    global _vosk_model
    if _vosk_model is None:
        if not os.path.exists(config.VOSK_MODEL_PATH):
            print(f"❌ Error: Vosk model not found at {config.VOSK_MODEL_PATH}")
            sys.exit(1)
        
        print("⚡ Loading Hindi Language Model (RAM Intensive)...")
        _vosk_model = Model(config.VOSK_MODEL_PATH)
        print("✅ Ears Ready.")
    return _vosk_model

def listen():
    """Opens a clean mic stream and returns transcribed text."""
    # 1. Ensure model is ready
    model = load_model()
    rec = KaldiRecognizer(model, config.SAMPLE_RATE)
    
    print("   (Listening for command...)")
    
    # 2. Open a temporary stream for the command
    # Using 'device=1' for your USB soundcard
    with sd.RawInputStream(samplerate=16000, 
                           blocksize=8000, 
                           device=None,
                           dtype='int16', 
                           channels=1) as stream:
        
        # We'll listen for a maximum of 5 seconds
        for _ in range(0, int(config.SAMPLE_RATE / 4000 * 5)):
            data, overflow = stream.read(4000)
            if rec.AcceptWaveform(bytes(data)):
                result = json.loads(rec.Result())
                return result.get('text', '').lower()
        
        # If silence or timeout
        final_result = json.loads(rec.FinalResult())
        return final_result.get('text', '').lower()
