import streamlit as st
from core.document_reader import extract_text
from core.agent import generate_summary
from core.translation import translate_text

st.set_page_config(page_title="Bhavini Prototype", layout="wide")
st.title("Bhavini – Document Intelligence Prototype")

TARGET_LANGUAGE_CODE = "te"   # hard-coded (Telugu)

uploaded_file = st.file_uploader(
    "Upload a government document (PDF)",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Reading document..."):
        text = extract_text(uploaded_file)

    st.subheader("Extracted Text")
    st.text_area("", text, height=300)

    with st.spinner("Generating summary..."):
        summary_en = generate_summary(text)

    with st.spinner("Translating summary using Bhashini..."):
        summary_translated = translate_text(
            text=summary_en,
            target_lang=TARGET_LANGUAGE_CODE
        )

    st.subheader("Summary")
    st.write(summary_translated)
