# uncompyle6 version 3.9.1
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
# Embedded file name: myVoice.py
# Compiled at: 2024-02-07 09:55:54
# Size of source mod 2**32: 1401 bytes
from time import sleep
from _thread import start_new_thread
try:
    import pyttsx3
    speakEn = True
except Exception as e:
    speakEn = False

class textToSpeed:

    def __init__(self):
        self.texts = []
        self.speaking = False
        if speakEn:
            start_new_thread(self.voiceBroadcast_Thread, ())

    def speak(self, text, wait=True):
        if speakEn:
            self.texts.append(text)
            self.speaking = True
        else:
            self.speaking = False
            wait = False
        if wait:
            while self.speaking:
                sleep(0.1)

    def voiceBroadcast_Thread(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 200)
        self.engine.setProperty("volume", 1.0)
        self.engine.setProperty("voice", self.engine.getProperty("voices")[0].id)
        while True:
            while len(self.texts):
                text = self.texts[0]
                del self.texts[0]
                self.engine.say(text)
                self.engine.runAndWait()
                self.engine.stop()
                self.speaking = True

            self.speaking = False
            sleep(0.1)
