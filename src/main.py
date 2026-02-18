import sounddevice as sd
import numpy as np
import os
import sys
import datetime

# Local imports
import config
import wakeword
# Note: We do NOT import stt or tts here to save RAM

def main():
    print("\n" + "="*30)
    print("   DHWANI (Pi Lite Edition)   ")
    print("="*30)

    # 1. Load the lightweight Wake Word model first
    if not wakeword.load_model():
        print("❌ Failed to load Wake Word engine.")
        return
    
    # Check if we are using the correct USB device ID
    # device=1 is standard for USB soundcards on Pi
    USB_MIC_ID = 1 

    print("\n✅ System Ready.")
    print(f"🎙️  Listening on Device {USB_MIC_ID} for 'Hey Jarvis'...")

    while True:
        try:
            # --- PHASE 1: WAKE WORD DETECTION ---
            # We open the mic stream just for detection
            with sd.InputStream(device=None,
                                channels=1, 
                                samplerate=16000, 
                                blocksize=config.CHUNK_SIZE) as stream:
                
                while True:
                    data, overflow = stream.read(config.CHUNK_SIZE)
                    if wakeword.detect(data):
                        print("\n✨ WAKE WORD DETECTED! ✨")
                        # Instant beep using system tool (fast)
                        os.system("aplay -q /usr/share/sounds/alsa/Front_Center.wav &")
                        break # Exit the 'with' block to close the mic stream
            
            # --- PHASE 2: LAZY LOAD HEAVY MODELS ---
            # Now that we know the user is talking, we load the ears
            print("⚡ Waking up STT engine...")
            import stt 
            import tts
            
            print("🗣️  Dhwani: Ji?")
            command = stt.listen()
            print(f"User said: {command}")

            # --- PHASE 3: COMMAND LOGIC ---
            if not command:
                print(">> (No speech detected)")
            
            elif "time" in command or "samay" in command:
                now = datetime.datetime.now().strftime("%I:%M %p")
                tts.speak(f"Sir, the time is {now}")

            elif "namaste" in command or "hello" in command:
                tts.speak("Namaste! Kaise hain aap?")

            elif "stop" in command or "exit" in command:
                tts.speak("Goodbye, Sir.")
                sys.exit(0)
            
            else:
                tts.speak(f"You said: {command}")
            
            print("\n🎙️  Returning to standby...")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Restarting in 2 seconds...")
            import time
            time.sleep(2)

if __name__ == "__main__":
    main()
