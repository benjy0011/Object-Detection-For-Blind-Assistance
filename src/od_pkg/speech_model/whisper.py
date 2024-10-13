import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import sounddevice as sd
import re

## initiallization
# get device number for speechrecognition
class Whisper:
    def __init__(self):
        pattern = f'([0-9])*[ ]*USB' # if using usb mic

        try:
            device = re.search(pattern, str(sd.query_devices())).group(1)
            self.DEVICE = int(device)
            print('\nUSB device number:',device)
        except AttributeError:
            print("AttributeError")

        # setting parameters
        device_info = sd.query_devices(self.DEVICE, "input")
        self.SAMPLERATE = int(device_info["default_samplerate"])
        self.ENERGY = 300
        self.PAUSE = 0.8
        self.DYNAMIC = False

        # setting up model
        model = "tiny.en"
        self.audio_model = whisper.load_model(model) 

        # load the speech recognizer and set the initial energy threshold and pause threshold
        self.r = sr.Recognizer()
        self.r.energy_threshold = self.ENERGY
        self.r.pause_threshold = self.PAUSE
        self.r.dynamic_energy_threshold = self.DYNAMIC

        # setup temporary directory
        temp_dir = tempfile.mkdtemp()
        self.save_path = os.path.join(temp_dir, "temp.wav")

        self.predicted_text = ""  

    def listen(self):                     
        with sr.Microphone(device_index=self.DEVICE, sample_rate=self.SAMPLERATE) as source:
            #get and save audio to wav file
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(self.save_path, format="wav")

            result = self.audio_model.transcribe(self.save_path)
            self.predicted_text = result["text"]

        return self.predicted_text