import streamlit as st
from core.document_reader import extract_text
from core.agent import generate_summary
from core.translation import translate_text

st.set_page_config(page_title="Bhavini Prototype", layout="wide")

INDIAN_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Odia": "or",
    "Assamese": "as",
    "Urdu": "ur",
    "Sanskrit": "sa",
    "Konkani": "kok",
    "Maithili": "mai",
    "Nepali": "ne",
    "Bodo": "brx",
    "Santhali": "sat",
    "Kashmiri": "ks",
    "Sindhi": "sd",
    "Manipuri (Meitei)": "mni"
}

# ---------- LANGUAGE SELECTION SCREEN ----------
if "language_selected" not in st.session_state:
    st.session_state.language_selected = False

if not st.session_state.language_selected:
    st.title("Welcome to Bhavini")
    st.subheader("Select your preferred language")

    selected_language = st.selectbox(
        "Language",
        list(INDIAN_LANGUAGES.keys())
    )

    if st.button("Continue"):
        st.session_state.language = selected_language
        st.session_state.language_code = INDIAN_LANGUAGES[selected_language]
        st.session_state.language_selected = True
        st.rerun()

    st.stop()

# ---------- MAIN APP ----------
st.title("Bhavini – Document Intelligence Prototype")
st.caption(f"Selected Language: {st.session_state.language}")

uploaded_file = st.file_uploader("Upload a government document (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading document..."):
        text = extract_text(uploaded_file)

    st.subheader("Extracted Text")
    st.text_area("Content", text, height=300, label_visibility="collapsed")

    if not text:
        st.error("Could not extract text from this document. It might be an image-only PDF. Please upload a PDF with selectable text.")
        st.stop()

    with st.spinner("Generating summary..."):
        summary_en = generate_summary(text)

    with st.spinner("Translating summary using Bhashini..."):
        summary_translated = translate_text(
            text=summary_en,
            target_lang=st.session_state.language_code
        )

    st.subheader("Summary")
    st.write(summary_translated)
