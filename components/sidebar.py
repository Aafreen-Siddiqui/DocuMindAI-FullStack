import streamlit as st
from urllib.parse import urlparse


def is_valid_url(url):
    parsed = urlparse(url.strip())

    return (
        parsed.scheme in ("http", "https")
        and "." in parsed.netloc
    )


def show_sidebar():
    st.sidebar.title("📄 DocuMind AI")

    source_type = st.sidebar.radio(
        "Choose source type",
        ["Upload document", "Website URL"],
        key="source_type"
    )

    if source_type == "Upload document":

        uploaded_file = st.sidebar.file_uploader(
            "Upload a document",
            type=["pdf", "csv", "txt"],
            key="document_uploader"
        )

        if uploaded_file is not None:
            st.sidebar.success(
                f"Uploaded: {uploaded_file.name}"
            )

        return uploaded_file

    else:

        url = st.sidebar.text_input(
            "Enter Website URL",
            key="website_url"
        )

        if url:

            if is_valid_url(url):
                return url

            st.sidebar.error(
                "Please enter a valid URL."
            )

        return None