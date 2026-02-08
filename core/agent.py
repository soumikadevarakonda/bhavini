# core/agent.py
import os
import google.generativeai as genai

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY") or "AIzaSyCEupAEHHAhC7DTX16p07TVpSuqjCvkdJM"
genai.configure(api_key=api_key)

# Use Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
        "Summarize government documents clearly and accurately. "
        "Use neutral, factual English. Avoid interpretation."
    )
)

def generate_summary(text: str) -> str:
    response = model.generate_content(
        text,
        generation_config={
            "temperature": 0.2,
        }
    )

    return response.text.strip()
