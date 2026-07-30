import streamlit as st
from urllib.parse import urlparse


def is_valid_url(url):
    parsed = urlparse(url)
    return (
        parsed.scheme in ("http", "https")
        and "." in parsed.netloc
    )

def show_sidebar():
    st.sidebar.title("📄 DocuMind AI")

    uploaded_file = st.sidebar.file_uploader(
        "Upload a document",
        type=["pdf", "csv", "txt"]
    )

    st.sidebar.markdown("---")
    st.sidebar.write("**OR**")

    url = st.sidebar.text_input("Enter Website URL")

    if uploaded_file:
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")
        return uploaded_file

    if url:
        if is_valid_url(url):
            return url
        else:
            st.sidebar.error("Please enter a valid URL.")

    return None