import google.generativeai as genai

def answer_question_from_document(
    document_text: str,
    question: str
) -> str:
    prompt = f"""
You are a government document assistant.

RULES (VERY IMPORTANT):
- Answer ONLY using the information in the document below
- If the document does NOT contain the answer, reply exactly:
  "The document does not contain this information."
- Do NOT use outside knowledge
- Do NOT guess
- Keep answers factual and concise

DOCUMENT:
{document_text}

QUESTION:
{question}
"""

    response = genai.GenerativeModel(
        model_name="gemini-2.5-flash"
    ).generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )

    return response.text.strip()
