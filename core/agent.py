from core.summarizer import summarize

def process_document(text):
    summary = summarize(text)

    return {
        "summary": summary
    }
