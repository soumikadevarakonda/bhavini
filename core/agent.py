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

def answer_question(context: str, question: str) -> str:
    """
    Answers a question based on the provided document context.
    """
    prompt = f"Document Content:\n{context}\n\nQuestion: {question}\n\nAnswer (keep it simple and direct):"
    
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
        }
    )
    return response.text.strip()
