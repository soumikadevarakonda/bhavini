import streamlit as st
from core.document_reader import extract_text
from core.agent import process_document

st.set_page_config(page_title="Bhavini Prototype", layout="wide")
st.title("Bhavini – Document Intelligence Prototype")

uploaded_file = st.file_uploader("Upload a government document (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading document..."):
        text = extract_text(uploaded_file)

    st.subheader("Extracted Text")
    st.text_area("", text, height=300)

    if st.button("Generate Summary"):
        with st.spinner("Summarizing..."):
            result = process_document(text)

        st.subheader("Summary")
        st.write(result["summary"])
