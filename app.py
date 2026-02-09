import streamlit as st
from core.document_reader import extract_text
from core.agent import generate_summary, answer_question
from core.translation import translate_text
from core.audio import text_to_audio, audio_to_text
from streamlit_audiorecorder import audiorecorder

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

    if not text:
        st.error("Could not extract text from this document. It might be an image-only PDF. Please upload a PDF with selectable text.")
        st.stop()

    with st.spinner("Generating summary..."):
        summary_en = generate_summary(text)

    # --- VOICE OUTPUT (TTS) ---
    st.subheader("Summary")
    st.write(summary_en) # Showing English summary for now as translation is mocked

    if st.button("🔊 Listen to Summary"):
        with st.spinner("Generating audio..."):
            audio_fp = text_to_audio(summary_en, "en")
            if audio_fp:
                st.audio(audio_fp, format='audio/mp3')

    # --- VOICE INPUT (Q&A) ---
    st.divider()
    st.subheader("Ask a Question (Voice)")

    audio_bytes = audiorecorder("Click to Record", "Recording...")
    
    if len(audio_bytes) > 0:
        st.audio(audio_bytes, format="audio/wav")
        
        with st.spinner("Transcribing..."):
            question_text = audio_to_text(audio_bytes)
        
        if question_text:
            st.success(f"You asked: {question_text}")
            
            with st.spinner("Getting answer..."):
                answer = answer_question(text, question_text)
            
            st.write(f"**Answer:** {answer}")
             
            # Auto-play answer
            answer_audio = text_to_audio(answer, "en")
            if answer_audio:
                st.audio(answer_audio, format='audio/mp3')
        else:
            st.warning("Could not understand audio. Please try again.")
