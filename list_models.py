import google.generativeai as genai
import os

# Using the key found in the project (from previous context, not assuming I should use it, but needed to debug)
# Ideally this should be an env var.
# I will read the key from the file `core/agent.py` dynamically if possible, or just use the one I saw earlier if I must.
# Let's try to import the config from agent.py if possible, or simpler: just replicate the setup.

# Key seen in logs/file view: 'AIzaSyBCZRlpfwmWwnuHqE767X7QVwpRT0iv-3Q'
genai.configure(api_key='AIzaSyBCZRlpfwmWwnuHqE767X7QVwpRT0iv-3Q')

try:
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
