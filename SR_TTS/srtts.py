# SRAndTTS
#
# Speech Recognize and Text to Speech

# @refer https://github.com/alphacep/vosk-api/
# @refer https://github.com/nateshmbhat/pyttsx3

import wave
from vosk import Model, KaldiRecognizer, SetLogLevel

wf = wave.open('test.wav', "rb")

model = Model("vosk-model-small-cn-0.3")
rec = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())


import pyttsx3
engine = pyttsx3.init()
engine.say('Hello, 2020')
engine.say('你好，上海自来水来自海上')
engine.runAndWait()
engine.stop()