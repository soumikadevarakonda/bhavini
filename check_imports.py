try:
    import gtts
    print("gtts: imported")
except ImportError as e:
    print(f"gtts: FAILED ({e})")

try:
    import speech_recognition
    print("speech_recognition: imported")
except ImportError as e:
    print(f"speech_recognition: FAILED ({e})")

try:
    import streamlit_audiorecorder
    print("streamlit_audiorecorder: imported")
except ImportError as e:
    print(f"streamlit_audiorecorder: FAILED ({e})")

try:
    import pydub
    print("pydub: imported")
except ImportError as e:
    print(f"pydub: FAILED ({e})")

try:
    import pytesseract
    print("pytesseract: imported")
except ImportError as e:
    print(f"pytesseract: FAILED ({e})")
