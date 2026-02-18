import os
import subprocess
import config

def speak(text):
    """Speaks the text using Piper (Hindi)"""
    print(f"🗣️ Dhwani: {text}")
    
    # Command to pipe text -> piper -> aplay (speaker)
    command = f'echo "{text}" | "{config.PIPER_PATH}" --model "{config.TTS_MODEL}" --output_raw | aplay -r 22050 -f S16_LE -t raw -'
    
    # Run silently
    subprocess.run(command, shell=True)
