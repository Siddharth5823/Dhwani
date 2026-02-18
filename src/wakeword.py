import os
from pocketsphinx import LiveSpeech

def detect():

    base_dir = os.path.dirname(os.path.dirname(__file__))
    dict_path = os.path.join(base_dir, 'assets', 'dhwani.dict')
    
    speech = LiveSpeech(
        keyphrase='dhwani',
        kws_threshold=1e-20,
        dict=dict_path 
    )
    
    for phrase in speech:
        if 'dhwani' in str(phrase):
            return True
    return False
