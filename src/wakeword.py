import os
from pocketsphinx import LiveSpeech
import sounddevice as sd

def get_pulse_device_id():
    # Loop through all audio devices
    for index, device in enumerate(sd.query_devices()):
        # If the name contains 'pulse', return that index
        if 'pulse' in device['name'].lower():
            return index
    return None # Fallback just in case

PULSE_ID = get_pulse_device_id()

def detect():

    base_dir = os.path.dirname(os.path.dirname(__file__))
    dict_path = os.path.join(base_dir, 'assets', 'dhwani.dict')
    
    speech = LiveSpeech(
        keyphrase='dhwani',
        kws_threshold=1e-20,
        dict=dict_path,
        audio_device=PULSE_ID
    )
    
    for phrase in speech:
        if 'dhwani' in str(phrase):
            return True
    return False
