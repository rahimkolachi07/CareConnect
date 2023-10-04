from flask import request
from flask_socketio import emit

from .extensions import socketio

users = {}

from googletrans import Translator

def translate_text(text, dest_language):
    """
    Translates the given text to the specified destination language using the Google Translate API.

    Parameters:
    text (str): The text to translate.
    dest_language (str): The destination language (as an ISO 639-1 code) to translate the text to.

    Returns:
    str: The translated text.
    """
    supported_languages = ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "ar", "hi", "tr", "nl", "el", "he", "pl", "sv", "th", "vi"]
    if dest_language not in supported_languages:
        return "Error: Unsupported destination language."

    translator = Translator()

    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        return f"Error: {str(e)}"



@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
@socketio.on("new_message")
def handle_new_message(data):
    if not data or not isinstance(data, dict):
        print("Error: received invalid data")
        return

    message = data.get('message')
    if not message:
        print("Error: no message in data")
        return

    translated_message = translate_text(message, "es")
    print(f"New message: {translated_message}")

    username = None 
    for user in users:
        if users[user] == request.sid:
            username = user
            break

    if not username:
        print("Error: no username found for SID")
        return

    emit("chat", {"message": translated_message, "username": username}, broadcast=True)
