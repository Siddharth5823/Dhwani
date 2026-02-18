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