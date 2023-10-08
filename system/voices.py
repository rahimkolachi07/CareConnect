import torch
from TTS.api import TTS
device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = TTS().list_models()[0]
tts = TTS(model_name).to(device)

wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])

tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")