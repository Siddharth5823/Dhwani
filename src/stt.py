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
