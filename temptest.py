import speech_recognition as sr

def speech_to_text_sr():
    """
    Transcribes speech from microphone input using the SpeechRecognition library.

    Returns:
        str: The transcribed text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

text = speech_to_text_sr()
print(text)