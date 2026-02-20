import os
import sys
from time import sleep
import wakeword
import datetime
import random

print("⚡Loading Hindi ASR Model...")
import stt
from tts import speak


def logic(command):
    if any(word in command for word in ["खतम ", "बंद", "मर","खत्म"]):
        print("ठीक है.....मैं जाती हूँ")
        speak("ठीक है.....मैं जाती हूँ")
        return False

    elif any(word in command for word in ["कैसी ", "केसी","कसी"]):
        print("मैं अच्छी हूँ")
        speak("मैं अच्छी हूँ")
    
    elif any(word in command for word in ["समय ","टाइम"]):
        now = datetime.datetime.now()
        print(f"अभी {now.hour} बज कर {now.minute} मिनट हो रहे हैं।")
        speak(f"अभी {now.hour} बज कर {now.minute} मिनट हो रहे हैं।")

    elif any(word in command for word in ["तारीख ","दिन","डेट"]):
        now = datetime.datetime.now()
        print(f"आज {now.day} तारीख है।")
        speak(f"आज {now.day} तारीख है।")

    elif any(word in command for word in ["तुम्हारा ", "नाम"]):
        print("मेरा नाम ध्वनि है। मैं एक पूरी तरह से ऑफलाइन एआई असिस्टेंट हूँ।")
        speak("मेरा नाम ध्वनि है। मैं एक पूरी तरह से ऑफलाइन एआई असिस्टेंट हूँ।")

    elif any(word in command for word in ["तुम्हें ", "किसने", "बनाया"]):
        print("मुझे आपने अपने प्रोजेक्ट के लिए बनाया है।")
        speak("मुझे आपने अपने प्रोजेक्ट के लिए बनाया है।")
    
    elif any(word in command for word in ["जोक ", "चुटकुला", "सुना"]):
        jokes = [
            "एक कंप्यूटर ने दूसरे कंप्यूटर से कहा, यार आज तो मदरबोर्ड खराब हो गया!",
            "प्रोग्रामर कभी सोते नहीं, वो बस स्लीप मोड में जाते हैं।",
            "मैंने एक एआई से पूछा कि प्यार क्या है? उसने एरर चार सौ चार (404) दे दिया!"
        ]
        joke = random.choice(jokes)
        print(joke)
        speak(joke)

    elif any(word in command for word in ["तुम ", "सुंदर","अच्छी"]): 
        print("धन्यवाद! यह सब आपकी शानदार प्रोग्रामिंग का नतीजा है।")
        speak("धन्यवाद! यह सब आपकी शानदार प्रोग्रामिंग का नतीजा है।")

    elif any(word in command for word in ["बहुत ", "उदास"]):
        print("टेंशन मत लीजिए! आप एक शानदार इंजीनियर हैं, बस अपने कोड पर फोकस रखिए।")
        speak("टेंशन मत लीजिए! आप एक शानदार इंजीनियर हैं, बस अपने कोड पर फोकस रखिए।")

    elif any(word in command for word in ["भूख "]):
        print("क्या हॉस्टल की मेस का खाना खाना है, या फिर एफ सी रोड जाकर कुछ खाएं?")
        speak("क्या हॉस्टल की मेस का खाना खाना है, या फिर एफ सी रोड जाकर कुछ खाएं?")

    return True



def main():
    print("\n" + "="*37)
    print("   DHWANI: Hindi ChatBot (Offline)   ")
    print("="*37)
    x = True
    while x:
        try:
            print("\nWaiting for Wake-Word Dhwani")
            if wakeword.detect():
                print("\nDETECTED!")
                command = stt.listen()
                if command:
                    print(f"User: {command}")
                    x = logic(command)       
                else:
                    print("No speech detected")
                sleep(0.5)
                
        except Exception as e:
            print(f"Error: {e}")
            sleep(2)

if __name__ == "__main__":
    main()
