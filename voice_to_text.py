import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print('speak')
    audio = r.listen(source)
print(r.recognize_google(audio))