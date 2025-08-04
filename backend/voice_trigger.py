import os
import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Say 'spin bot activated'...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("🗣️ You said:", command)
        return command
    except:
        return ""

while True:
    if "spin bot activated" in listen():
        print("🧠 Voice trigger activated!")
        os.system("python3 ~/dardy_empire/backend/sniper_loop.py")
