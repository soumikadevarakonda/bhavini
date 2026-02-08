from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="facebook/bart-large-cnn"
)

def summarize(text):
    text = text[:3000]

    prompt = (
        "Summarize the following document in clear, simple language.\n\n"
        f"{text}\n\nSummary:"
    )

    output = generator(
        prompt,
        max_new_tokens=150,
        do_sample=False
    )

    return output[0]["generated_text"].split("Summary:")[-1].strip()
