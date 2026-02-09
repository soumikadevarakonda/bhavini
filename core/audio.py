import os
from gtts import gTTS
import speech_recognition as sr
import io

def text_to_audio(text: str, language_code: str) -> io.BytesIO:
    """
    Converts text to audio using Google Text-to-Speech (gTTS).
    Returns audio data as BytesIO object.
    """
    try:
        # Map Bhashini/standard codes to gTTS codes if necessary
        # gTTS uses standard ISO codes mostly (hi, en, ta, etc.)
        tts = gTTS(text=text, lang=language_code, slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

def audio_to_text(audio_bytes: bytes) -> str:
    """
    Converts audio bytes to text using Google Speech Recognition.
    """
    r = sr.Recognizer()
    
    # Needs a file-like object
    audio_file = io.BytesIO(audio_bytes)
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            # Recognize speech using Google Web Speech API
            # default language is English, can be parameterized later
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "" # Could not understand audio
    except sr.RequestError as e:
        print(f"STT Error: {e}")
        return ""
    except Exception as e:
        print(f"General STT Error: {e}")
        return ""
