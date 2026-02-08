# core/translation.py
import requests

BHASHINI_API_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
BHASHINI_API_KEY = "YOUR_API_KEY"

def translate_text(text: str, target_lang: str) -> str:
    payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "en",
                        "targetLanguage": target_lang
                    }
                }
            }
        ],
        "inputData": {
            "input": [
                {"source": text}
            ]
        }
    }

    headers = {
        "Authorization": BHASHINI_API_KEY,
        "Content-Type": "application/json"
    }

    # response = requests.post(
    #     BHASHINI_API_URL,
    #     headers=headers,
    #     json=payload,
    #     timeout=30
    # )

    # response.raise_for_status()
    #data = response.json()

    #return data["pipelineResponse"][0]["output"][0]["target"]
    return text
