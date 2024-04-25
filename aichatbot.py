import google.generativeai as genai
# import whisper
import pyttsx3
import speech_recognition as sr
import mypandasfile

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

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



# Replace with your actual API key from AI Studio
API_KEY = "AIzaSyACTuQ6H1p45h3LTwLtOKXB3ORQQGlb_iU"

def initialize_api():
    """
    Initializes the connection to Gemini 1.5 Pro API
    """
    try:
      genai.configure(api_key=API_KEY)
    except Exception as e:
      print(f"An error occurred during API configuration: {e}")
      exit(1)

def generate_response(prompt):
    """
    Sends a prompt to Gemini 1.5 Pro and retrieves the response
    """
    # Set up the model generation configuration
    generation_config = {
        "temperature": 0.7,  # Adjust for more creative or informative responses (0-1)
        "top_p": 1,
        "top_k": 10,
        "max_output_tokens": 200048,  # Maximum number of tokens in the response
    }

    # Specify the model name (v1beta for preview access)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config)
  
    # Send the prompt as a list
    prompt_parts = [prompt]
  
    try:
      response = model.generate_content(prompt_parts)
      return response.text
    except Exception as e:
      print(f"An error occurred during generation: {e}")
      return None

if __name__ == "__main__":
    # while True:
    #     print('Say something')
    #     text = speech_to_text_st()
    #     if text:
    #         # print(text)
    #         # Here, you would process the text with your chatbot logic
    #         response = "This is where your chatbot would generate a response based on the user's input."
            # text_to_speech(response)
    initialize_api()
    # with open("output.txt", "r") as f:
    #     code_text = f.read()

    # cdf = mypandasfile.get_all_list()
    # cdfx = cdf.to_json()
    # print("-"*100)
    # cdf = f"RESPONSE IN HINGLISH \n Here is the data of customers in json format, tell me a report of lilu \n {cdfx}"
    # print(generate_response(cdf))
    while 1:
        prompt = input("Enter your prompt for Gemini 1.5 Pro: ")
        if prompt == "q":
            break
        else:
            response = generate_response(prompt)
            if response:
                print(f"Gemini 1.5 Pro responded: \n{response}")
            else:
                print("An error occurred, please try again.")