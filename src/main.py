import os
import sys
from time import sleep
import wakeword

print("⚡Loading Hindi ASR Model...")
import stt
from tts import speak

def main():
    print("\n" + "="*37)
    print("   DHWANI: Hindi ChatBot (Offline)   ")
    print("="*37)

    while True:
        try:
            print("\nWaiting for Wake-Word Dhwani")
            if wakeword.detect():
                print("\nDETECTED!")
                
                #os.system("aplay -q /usr/share/sounds/alsa/Front_Center.wav &")
                command = stt.listen()
                
                if command:
                    print(f"User: {command}")
                    if any(word in command for word in ["खतम ", "बंद", "मर","खत्म"]):
                        speak("ठीक है.....मैं जाती हूँ")
                        break      
                    if any(word in command for word in ["कैसी ", "हो", "केसी","कसी","हा"]):
                        speak("मैं आपकी मैया चोद दूंगी")
                else:
                    print("No speech detected")

                sleep(0.5)
                
        except Exception as e:
            print(f"Error: {e}")
            sleep(2)

if __name__ == "__main__":
    main()
