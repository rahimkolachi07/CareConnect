import speech_recognition as sr
import pyttsx3
import openai

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

def respond(command,company):
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
            {"role": "system", "content": f"your company is {company}"},
            {"role": "system", "content": "show expressions as humans do"},
            {"role": "system", "content": "response must be shorter as possible as"},
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
    company=input("INPUT YOUR COMPANY Name")
    while True:
        audio = listen()
        command = recognize(audio)
        if None == command:
            pass
        else:
            respond(command,company)
