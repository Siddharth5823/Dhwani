'''
import subprocess
import config
import json
import time
import sys

pipe_proc = None

def init_tts():
    global pipe_proc
    if pipe_proc is None:
        pipe_proc = subprocess.Popen(
            [config.PIPER_PATH, "--model", config.TTS_MODEL, "--output_raw", "--json-input"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0 
        )

def speak(text):
    global pipe_proc
    if pipe_proc is None: init_tts()
    
    # 1. Start player with 'stderr' hidden to stop the 'Playing raw data' message
    player = subprocess.Popen(
        ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "--buffer-time", "50000"],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL  # <--- THIS REMOVES THE 2nd LINE OUTPUT
    )

    # 2. Prepare the payload
    msg = json.dumps({"text": text}) + "\n"
    pipe_proc.stdin.write(msg.encode("utf-8"))
    pipe_proc.stdin.flush()

    # 3. Print the text ONLY after we start feeding audio to the player
    # This reduces the perceived 'latency' gap
    print(f"Dhwani: {text}", flush=True)

    # 4. Stream the audio
    while True:
        chunk = pipe_proc.stdout.read(4096)
        if not chunk: break
        player.stdin.write(chunk)
        if len(chunk) < 4096: break

    # 5. Wait for speech to finish before returning to main
    player.stdin.close()
    player.wait()

init_tts()

import subprocess
import config
import json

pipe_proc = None

def init_tts():
    global pipe_proc
    
    # If the process is dead, clear it so it restarts
    if pipe_proc is not None and pipe_proc.poll() is not None:
        pipe_proc = None

    if pipe_proc is None:
        pipe_proc = subprocess.Popen(
            [config.PIPER_PATH, "--model", config.TTS_MODEL, "--output_raw", "--json-input"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            # We REMOVED stderr=DEVNULL here so we can actually see if Piper throws an error!
            bufsize=0 
        )

def speak(text):
    global pipe_proc
    init_tts() # Ensure Piper is alive before speaking
    
    print(f"Dhwani: {text}", flush=True)

    msg = json.dumps({"text": text}) + "\n"
    
    # The Self-Healing Try/Catch Block
    try:
        pipe_proc.stdin.write(msg.encode("utf-8"))
        pipe_proc.stdin.flush()
    except BrokenPipeError:
        print("⚠️ Piper background process died. Restarting...")
        init_tts()
        pipe_proc.stdin.write(msg.encode("utf-8"))
        pipe_proc.stdin.flush()

    # Start the audio player (we keep this one quiet)
    player = subprocess.Popen(
        ["aplay", "-D", "pulse", "-r", "22050", "-f", "S16_LE", "-t", "raw", "--buffer-time", "50000"],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL 
    )

    # Stream the audio
    while True:
        chunk = pipe_proc.stdout.read(4096)
        if not chunk: break
        player.stdin.write(chunk)
        if len(chunk) < 4096: break

    player.stdin.close()
    player.wait()

init_tts()

'''
import subprocess
import config
import json

pipe_proc = None

def init_tts():
    global pipe_proc
    if pipe_proc is not None and pipe_proc.poll() is not None:
        pipe_proc = None

    if pipe_proc is None:
        pipe_proc = subprocess.Popen(
            [config.PIPER_PATH, "--model", config.TTS_MODEL, "--output_raw", "--json-input"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0 
        )

def speak(text):
    global pipe_proc
    if pipe_proc is None or pipe_proc.poll() is not None:
        init_tts()
    
    # ---------------------------------------------------------
    # THE FIX: Remove punctuation so Piper doesn't micro-flush!
    # ---------------------------------------------------------
    clean_text = text.replace("!", " ").replace("।", " ").replace(",", " ").replace("?", " ")
    
    # We still print the original text with punctuation for the UI
    print(f"Dhwani: {text}", flush=True)

    # We send the clean text to Piper
    msg = json.dumps({"text": clean_text}) + "\n"
    
    try:
        pipe_proc.stdin.write(msg.encode("utf-8"))
        pipe_proc.stdin.flush()
    except BrokenPipeError:
        init_tts()
        pipe_proc.stdin.write(msg.encode("utf-8"))
        pipe_proc.stdin.flush()

    player = subprocess.Popen(
        ["aplay", "-D", "pulse", "-r", "22050", "-f", "S16_LE", "-t", "raw", "--buffer-time", "50000"],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL 
    )

    while True:
        chunk = pipe_proc.stdout.read(4096)
        if not chunk: break
        player.stdin.write(chunk)
        # Now it will only break when the ENTIRE sentence is finished
        if len(chunk) < 4096: break

    player.stdin.close()
    player.wait()

init_tts()