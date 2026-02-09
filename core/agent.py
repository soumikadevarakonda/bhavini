# core/agent.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
genai.configure(api_key=api_key)

import google.api_core.exceptions

# Use Gemini model
model_name = "gemini-2.5-flash"
model = genai.GenerativeModel(
    model_name=model_name,
    system_instruction=(
        "Summarize government documents clearly and accurately. "
        "Use neutral, factual English. Avoid interpretation."
    )
)

def _generate_safe(prompt: str, config: dict) -> str:
    try:
        response = model.generate_content(prompt, generation_config=config)
        return response.text.strip()
    except google.api_core.exceptions.ResourceExhausted:
        return (
            "⚠️ **API Quota Exceeded**: You have reached the free tier limit for Gemini API. "
            "Please wait a few minutes and try again. (Error 429)"
        )
    except Exception as e:
        return f"⚠️ **AI Error**: An unexpected error occurred: {str(e)}"

def generate_summary(text: str, language: str = "English") -> str:
    prompt = f"Summarize the following text in {language}. Keep it concise and factual:\n\n{text}"
    return _generate_safe(prompt, {"temperature": 0.2})

def answer_question(context: str, question: str, language: str = "English") -> str:
    """
    Answers a question based on the provided document context.
    """
    prompt = f"Document Content:\n{context}\n\nQuestion: {question}\n\nAnswer (in {language}, keep it simple and direct):"
    return _generate_safe(prompt, {"temperature": 0.3})
