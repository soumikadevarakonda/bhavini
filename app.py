import streamlit as st
from core.document_reader import extract_text
from core.agent import generate_summary
from core.translation import translate_text
from core.chat import answer_question_from_document

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Bhavini Prototype",
    layout="wide"
)

# ==================================================
# GLOBAL STYLES (CHAT APP LOOK)
# ==================================================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}

/* Card container */
.card {
    background: white;
    padding: 1.25rem;
    border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

/* ---------- CHAT ---------- */
.chat-box {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    max-height: 65vh;
    overflow-y: auto;
    padding-right: 6px;
}

.chat-bubble {
    max-width: 80%;
    padding: 0.7rem 0.9rem;
    border-radius: 14px;
    font-size: 0.95rem;
    line-height: 1.45;
    word-wrap: break-word;
}

/* Assistant (LEFT) */
.chat-assistant {
    align-self: flex-start;
    background: #f1f5f9;
    color: #0f172a;
    border-bottom-left-radius: 4px;
}

/* User (RIGHT) */
.chat-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    border-bottom-right-radius: 4px;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    border: 2px dashed #6366f1;
    border-radius: 12px;
    padding: 1rem;
}

button {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE MAP
# ==================================================
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

# ==================================================
# LANGUAGE SELECTION (ONBOARDING)
# ==================================================
if "language_selected" not in st.session_state:
    st.session_state.language_selected = False

if not st.session_state.language_selected:
    st.markdown("""
    <div class="card">
        <h1>🇮🇳 Bhavini</h1>
        <p style="font-size:1.1rem;color:#475569;">
            Understand government documents and ask questions
            in your preferred Indian language.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    selected_language = st.selectbox(
        "Choose your language",
        list(INDIAN_LANGUAGES.keys())
    )

    if st.button("Continue →"):
        st.session_state.language = selected_language
        st.session_state.language_code = INDIAN_LANGUAGES[selected_language]
        st.session_state.language_selected = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================================================
# MAIN APP
# ==================================================
st.title("Bhavini – Document Intelligence Prototype")
st.caption(f"Selected Language: {st.session_state.language}")

uploaded_file = st.file_uploader(
    "Upload a government document (PDF)",
    type=["pdf"]
)

if uploaded_file:
    # Reset chat on new document
    if (
        "last_file_name" not in st.session_state
        or st.session_state.last_file_name != uploaded_file.name
    ):
        st.session_state.chat_messages = []
        st.session_state.last_file_name = uploaded_file.name

    with st.spinner("Processing document..."):
        text = extract_text(uploaded_file)

    if not text:
        st.error("Could not extract text from this document.")
        st.stop()

    with st.spinner("Generating summary..."):
        summary_en = generate_summary(text)

    with st.spinner("Translating summary using Bhashini..."):
        summary_translated = translate_text(
            text=summary_en,
            target_lang=st.session_state.language_code
        )

    # ==================================================
    # TWO COLUMN LAYOUT
    # ==================================================
    left_col, right_col = st.columns([1.1, 1])

    # ---------------- SUMMARY ----------------
    with left_col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧾 Summary")
        st.write(summary_translated)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CHAT ----------------
    with right_col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💬 Ask questions")
        st.caption("Answers are generated strictly from the uploaded document.")

        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        # Render chat
        st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
        for msg in st.session_state.chat_messages:
            css_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
            st.markdown(
                f"<div class='chat-bubble {css_class}'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # Chat input
        user_question = st.chat_input("Ask a question about this document")

        if user_question:
            # Add user message immediately
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_question
            })

            with st.spinner("Answering..."):
                answer = answer_question_from_document(
                    document_text=text,
                    question=user_question
                )

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": answer
            })

            # Force rerender so user message is visible
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
