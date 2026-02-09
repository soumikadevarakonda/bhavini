import streamlit as st
from core.document_reader import extract_text
from core.agent import generate_summary, answer_question
from core.translation import translate_text
from core.audio import text_to_audio, audio_to_text
# from audiorecorder import audiorecorder # Removed in favor of st.audio_input
from dotenv import load_dotenv
import os

load_dotenv()

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

# Load Custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- SIDEBAR (NAVIGATION & SETTINGS) ----------
with st.sidebar:
    st.markdown("### 🏛️ Vahini PRO")
    
    st.markdown("---")
    st.markdown("**Settings**")
    
    # Language Selection
    selected_language = st.selectbox(
        "Interface Language",
        list(INDIAN_LANGUAGES.keys()),
        index=0
    )
    
    if st.button("Update Language", use_container_width=True):
        st.session_state.language = selected_language
        st.session_state.language_code = INDIAN_LANGUAGES[selected_language]
        st.session_state.language_selected = True
        st.rerun()

    st.markdown("---")
    st.info("System Status: Online 🟢")
    
    with st.expander("About"):
        st.caption("GovTech Inclusive AI Assistant v1.0")
        st.caption("© 2026 Vahini Project")

# ---------- MAIN HEADER ----------
st.markdown("<h1>🇮🇳 Vahini Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### Sovereign Translation & Analysis System for Indian Governments")
st.markdown("---")

# ---------- DASHBOARD GRID ----------
if "language_selected" not in st.session_state:
    st.session_state.language_selected = False
    st.session_state.language = "English"

# Row 1: Upload Widget
col_upload, col_info = st.columns([1, 2])

with col_upload:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("#### 📂 Upload Document")
    uploaded_file = st.file_uploader("Select PDF File", type=["pdf"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_info:
    if not uploaded_file:
         st.markdown('<div class="css-card">', unsafe_allow_html=True)
         st.markdown("#### 👋 Welcome Administrator")
         st.write("Please upload a Government Order (GO), Circular, or Form to begin analysis.")
         st.info("Supported formats: PDF (Text & Image-based)")
         st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    # Processing Logic
    with st.spinner("Processing document..."):
        text = extract_text(uploaded_file)

    if not text:
        st.error("Text extraction failed. Security restricted or empty PDF.")
        st.stop()

    # Row 2: Analysis Section (Tabs)
    st.markdown("### Document Intelligence")
    
    tab_summary, tab_qna, tab_source = st.tabs(["📝 Executive Summary", "🎙️ Voice Q&A", "📄 Source Text"])
    
    with tab_summary:
        with st.status("Generating insights...", expanded=True) as status:
            summary_en = generate_summary(text)
            status.update(label="Analysis Complete", state="complete", expanded=False)
        
        col_sum_text, col_sum_audio = st.columns([3, 1])
        with col_sum_text:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.info(summary_en)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_sum_audio:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.markdown("**Audio Playback**")
            if st.button("▶️ Read Aloud"):
                 audio_fp = text_to_audio(summary_en, "en")
                 if audio_fp:
                     st.audio(audio_fp)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_qna:
        col_qna_input, col_qna_res = st.columns([1, 2])
        
        with col_qna_input:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.markdown("**Ask a Question**")
            st.caption("Use your microphone to query the document.")
            audio_value = st.audio_input("Record Voice")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_qna_res:
            if audio_value:
                 with st.spinner("Analyzing query..."):
                    q_text = audio_to_text(audio_value.read())
                    if q_text:
                        st.markdown(f"**Query:** {q_text}")
                        ans = answer_question(text, q_text)
                        
                        st.success(f"Answer: {ans}")
                        
                        ans_audio = text_to_audio(ans, "en")
                        if ans_audio:
                            st.audio(ans_audio)
                    else:
                        st.warning("Audio not recognized.")
            else:
                st.info("Awaiting voice input...")

    with tab_source:
        st.text_area("Raw Extracted Text", text, height=300)

# Footer
st.markdown(
    """
    <div class="professional-footer">
        <strong>Vahini Project</strong> | Inclusive AI for India <br>
        Developed by Madhu Vadlamani, Pradeep Vadlamuri, Manikanta, Soumika
    </div>
    """,
    unsafe_allow_html=True
)
