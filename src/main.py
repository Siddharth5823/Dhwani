import sounddevice as sd
import queue
import sys
import time

# Custom Modules
import config
import wakeword
import stt
import tts
import datetime

# --- AUDIO QUEUE ---
q = queue.Queue()

def callback(indata, frames, time, status):
    """Puts audio into the queue efficiently"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def main():
    print("\n-------------------------")
    print("   DHWANI (Pi Edition)   ")
    print("-------------------------")

    # 1. SETUP: Load Models
    if not wakeword.load_model():
        return # Stop if wake word model is missing
    
    # (Optional) Verify other models exist
    # stt.init_model() # You might want to add an init function in stt.py too

    print("\n🎙️  System Online. Waiting for 'Hey Jarvis'...")

    # 2. MAIN LOOP
    # We open the mic stream ONCE. 
    # NOTE: To switch between Wake Word and STT on the same stream, 
    # we need to pass the audio data to the right function.
    
    with sd.RawInputStream(samplerate=config.SAMPLE_RATE, 
                           blocksize=config.CHUNK_SIZE, 
                           dtype='int16', 
                           channels=1, 
                           callback=callback):
        
        while True:
            # --- PHASE 1: WAKE WORD DETECTION ---
            chunk = q.get()
            
            if wakeword.detect(chunk):
                print("\n✨ WAKE WORD DETECTED! ✨")
                tts.speak("Ji?")  # Acknowledge
                
                # Clear queue so old audio doesn't confuse the command listener
                with q.mutex:
                    q.queue.clear()
                
                # --- PHASE 2: COMMAND LISTENING (Vosk) ---
                print("listening for command...")
                
                # We need a way to feed the SAME queue to STT
                # Ideally, stt.listen() should accept 'q' as an argument
                # or we temporarily handle STT logic here for simplicity.
                
                command = stt.listen_from_queue(q) # <--- We need to add this to stt.py
                print(f"User said: {command}")

                # --- PHASE 3: LOGIC ---
                if "time" in command:
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    tts.speak(f"Samay {now} hai")
                
                elif "namaste" in command:
                    tts.speak("Namaste! Kaise hain aap?")
                
                elif "exit" in command:
                    tts.speak("Alvida.")
                    break

                elif command == "":
                    tts.speak("Kuch sunayi nahi diya.")

                print("\n🎙️  Waiting for 'Hey Jarvis'...")

if __name__ == "__main__":
    main()
