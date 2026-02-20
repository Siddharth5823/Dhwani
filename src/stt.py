import sounddevice as sd
import json
import os
import sys
from vosk import Model, KaldiRecognizer
import config

_vosk_model = None

def get_pulse_device_id():
    # Loop through all audio devices
    for index, device in enumerate(sd.query_devices()):
        # If the name contains 'pulse', return that index
        if 'pulse' in device['name'].lower():
            return index
    return None # Fallback just in case

PULSE_ID = get_pulse_device_id()

def load_model():
    global _vosk_model
    if _vosk_model is None:
        if not os.path.exists(config.VOSK_MODEL_PATH):
            print(f"Error: Vosk model not found at {config.VOSK_MODEL_PATH}")
            sys.exit(1)
        
        print("Loading Hindi Language Model")
        _vosk_model = Model(config.VOSK_MODEL_PATH)
        print("ASR Ready.")
    return _vosk_model

model = load_model()

def listen():

    rec = KaldiRecognizer(model, config.SAMPLE_RATE)
    print("Listening for command")
    
    with sd.RawInputStream(samplerate=16000, 
                           blocksize=8000, 
                           device=PULSE_ID,
                           dtype='int16', 
                           channels=1) as stream:
        
        for _ in range(0, int(config.SAMPLE_RATE / 4000 * 5)):
            data, overflow = stream.read(4000)
            if rec.AcceptWaveform(bytes(data)):
                result = json.loads(rec.Result())
                hindi = result.get('text', '').lower()
                return hindi

        final_result = json.loads(rec.FinalResult())
        hindi = final_result.get('text', '').lower()
        return hindi
