import queue
import sys
import sounddevice as sd

from vosk import Model, KaldiRecognizer

import re

class Vosk:
    def __init__(self):
        # get device number for speechrecognition
        pattern = f'([0-9])*[ ]*USB' # if using usb mic

        try:
            device = re.search(pattern, str(sd.query_devices())).group(1)
            self.DEVICE = int(device)
            print('\nUSB device number:',device)
        except AttributeError:
            print("AttributeError")

        device_info = sd.query_devices(self.DEVICE, "input")
        self.SAMPLERATE = int(device_info["default_samplerate"])
        
        self.q = queue.Queue()
        
        model = Model(lang="en-us")
        self.rec = KaldiRecognizer(model, self.SAMPLERATE)  
        

    def listen(self):
        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            self.q.put(bytes(indata))
        
        recognized_speech = ""
        with sd.RawInputStream(samplerate=self.SAMPLERATE, 
                               blocksize = 8000, device=self.DEVICE,
                               dtype="int16", channels=1, callback=callback):
            data = self.q.get()
            if self.rec.AcceptWaveform(data):
                recognized_speech = self.rec.Result()[14:-3]
                
        return recognized_speech
    
    
if __name__ == "__main__":
    vo = Vosk()
    try:
        while True:
            speech = vo.listen()
            if speech != "":
                print(speech)
    
    except KeyboardInterrupt:
        print("Exiting......")