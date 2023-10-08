import speech_recognition as sr
import pyttsx3
import openai

# Set your API key here
openai.api_key = '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'

def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    
    return audio

def recognize(audio):
    recognizer = sr.Recognizer()
    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        return None

def respond(command):
    print(f"You said: {command}")
    
    # Using a prompt template
    prompt_template = f"""
    [Customer] {command}
    [Assistant]
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the GPT-3.5 Turbo engine
        messages=[
            {"role": "system", "content": "You are a customer care person"},
            {"role": "system", "content": "your company is PTCL"},
            {"role": "system", "content": "give response like customar care peope do, like greetings and endings"},
            {"role": "system", "content": "show expressions as humans do"},
            {"role": "system", "content": "response must be shorter as possible as"},
            {"role": "system", "content": "in last ask user is anything to ask if you asks then give response if user end the commnunication write thank you so much"},
            {"role": "user", "content": command}
        ]
    )
    reply = response['choices'][0]['message']['content'].strip()
    speak(reply)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        audio = listen()
        command = recognize(audio)
        if None == command:
            pass
        else:
            respond(command)
