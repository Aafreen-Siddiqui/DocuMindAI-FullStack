import time
import requests
import streamlit as st

from components.sidebar import show_sidebar


# -----------------------------------------
# Configuration
# -----------------------------------------

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide"
)


# -----------------------------------------
# API functions
# -----------------------------------------

def upload_document_to_api(source):
    """
    Upload either a file or a website URL to FastAPI.
    """

    if isinstance(source, str):
        # Web URL
        response = requests.post(
            f"{API_URL}/documents/upload",
            data={
                "source_url": source
            },
            timeout=60
        )

    else:
        # Uploaded file
        files = {
            "file": (
                source.name,
                source.getvalue(),
                source.type
            )
        }

        response = requests.post(
            f"{API_URL}/documents/upload",
            files=files,
            timeout=60
        )

    if response.status_code == 429:
        raise Exception(
            "Upload limit reached. Please try again later."
        )

    response.raise_for_status()

    return response.json()


def wait_for_ingestion(job_id):
    """
    Wait until FastAPI finishes document ingestion.
    """

    status_placeholder = st.empty()

    while True:

        response = requests.get(
            f"{API_URL}/documents/status/{job_id}",
            timeout=30
        )

        response.raise_for_status()

        status_data = response.json()
        status = status_data.get("status")

        if status == "queued":

            status_placeholder.info(
                "Document is waiting for processing..."
            )

        elif status == "processing":

            status_placeholder.info(
                "Loading document and creating embeddings..."
            )

        elif status == "completed":

            chunks = status_data.get("chunks", "unknown")

            status_placeholder.success(
                f"Document processed successfully. "
                f"Chunks created: {chunks}"
            )

            return True

        elif status == "failed":

            error_message = status_data.get(
                "error",
                "Document processing failed."
            )

            status_placeholder.error(error_message)

            return False

        time.sleep(1)


def ask_question_to_api(question, job_id):
    """
    Send a question to FastAPI.
    """

    payload = {
        "question": question,
        "job_id": job_id
    }

    response = requests.post(
        f"{API_URL}/questions/ask",
        json=payload,
        timeout=120
    )
    if response.status_code == 429:
        return {
                "success": False,
                "error_type": "rate_limit",
                "message": "⏳ Question limit reached. Please try again after 60 seconds."
            }

    response.raise_for_status()

    response_data = response.json()

    return response_data.get(
        "answer",
        "No answer was returned by the API."
    )


# -----------------------------------------
# Session state
# -----------------------------------------

if "job_id" not in st.session_state:
    st.session_state.job_id = None

if "current_source" not in st.session_state:
    st.session_state.current_source = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------------------
# Sidebar
# -----------------------------------------

source = show_sidebar()


# -----------------------------------------
# Upload and ingestion
# -----------------------------------------

if source is not None:

    if isinstance(source, str):
        # URL source
        source_identifier = source

    else:
        # Uploaded file source
        source_identifier = source.name

    # Process only when a new source is selected
    if st.session_state.current_source != source_identifier:

        st.session_state.current_source = source_identifier
        st.session_state.job_id = None
        st.session_state.chat_history = []

        try:

            with st.spinner("Sending source to FastAPI..."):

                upload_response = upload_document_to_api(source)

                job_id = upload_response.get("job_id")

                if not job_id:
                    st.error(
                        "FastAPI did not return a job ID."
                    )
                    st.stop()

                st.session_state.job_id = job_id

            ingestion_completed = wait_for_ingestion(job_id)

            if not ingestion_completed:
                st.session_state.job_id = None
                st.stop()

        except requests.RequestException as error:

            st.error(
                f"Could not communicate with FastAPI: {error}"
            )

            st.session_state.job_id = None
            st.stop()

        except Exception as error:

            st.error(
                f"An unexpected error occurred: {error}"
            )

            st.session_state.job_id = None
            st.stop()


# -----------------------------------------
# Main interface
# -----------------------------------------

st.title("📚 DocuMind AI")

st.write(
    "Upload a PDF, CSV, TXT document, or enter a website URL "
    "from the sidebar."
)


if st.session_state.job_id is None:

    st.info(
        "Please upload a document or enter a valid website URL "
        "from the sidebar to begin."
    )

else:

    st.success("Source is ready. You can now ask questions.")

    # Display previous conversation
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask a question about your document..."
    )

    if user_question:

        # Display user's question
        with st.chat_message("user"):
            st.markdown(user_question)

        # Save user's question locally for display
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        # Ask FastAPI
        with st.chat_message("assistant"):

            with st.spinner("Generating answer..."):

                try:

                    answer = ask_question_to_api(
                        question=user_question,
                        job_id=st.session_state.job_id
                    )

                    st.markdown(answer)

                    # Save assistant's answer locally for display
                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except requests.RequestException as error:

                    st.error(
                        f"Question request failed: {error}"
                    )