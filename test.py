import whisper
import speech_recognition as sr

# Load a model (e.g., small.en for English)
model = whisper.load_model("base.en")


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak something:")
    audio = r.listen(source, timeout=10)

with open("audio.wav", "wb") as file:
    file.write(audio.get_wav_data())
# Transcribe audio from a file
result = model.transcribe("audio.wav")
print(result["text"])

