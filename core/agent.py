# core/agent.py
import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key='AIzaSyBCZRlpfwmWwnuHqE767X7QVwpRT0iv-3Q')

# Use Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
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
