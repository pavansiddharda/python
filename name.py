import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from playsound import playsound
import os
import uuid
import time


def get_lang_code_from_name(lang_name):
    lang_name = lang_name.lower()
    for code, name in LANGUAGES.items():
        if name.lower() == lang_name:
            return code
    return None

def get_language_input(prompt):
    while True:
        lang_name = input(prompt).strip()
        lang_code = get_lang_code_from_name(lang_name)
        if lang_code:
            return lang_code
        else:
            print("Invalid language name. Please try again (e.g., English, Hindi, Telugu).")

def listen(lang_code='en'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Speak now)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio, language=lang_code)
        print(f"Original (Detected): {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError:
        print("Speech Recognition service unavailable")
        return None

def translate_text(text, target_language='en'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language)
        print(f"Translated ({target_language}): {translated.text}")
        return translated.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return None

def speak_text(text, lang='en'):
    try:
        filename = f"translated_audio_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        playsound(filename)
        time.sleep(1)
        os.remove(filename)
    except Exception as e:
        print(f"Text-to-speech failed: {e}")

def main():
    print("----- Real-Time Translator App (Now with Language Names) -----\n")

    input_lang = get_language_input("Enter the language YOU will SPEAK (e.g., English, Hindi, Telugu): ")

    spoken_text = listen(lang_code=input_lang)
    if not spoken_text:
        return

  
    target_lang = get_language_input("Enter the language to TRANSLATE into (e.g., Telugu, French, Tamil): ")

    translated_text = translate_text(spoken_text, target_language=target_lang)
    if translated_text:
        speak_text(translated_text, lang=target_lang)
# End of main()

if __name__ == "__main__":
    main()