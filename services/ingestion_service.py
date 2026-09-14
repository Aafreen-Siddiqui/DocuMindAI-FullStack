import os
import tempfile

from langchain_groq import ChatGroq
from utils.rag_chain import prompts_and_chains
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    WebBaseLoader
)

from utils.splitter import splitting_docs
from utils.embeddings import embed_docs
from utils.vectorStoreAndRetriever import (
    storing_vector_and_retriever
)


# Temporary in-memory stores
job_status = {}
retriever_store = {}
chain_store = {}
chat_history_store = {}


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def process_document_in_background(
    job_id: str,
    filename: str,
    content: bytes = None,
    source_url: str = None
):
    """
    Ingests either an uploaded file or a webpage URL.
    """

    temp_path = None

    try:
        job_status[job_id] = {
            "status": "processing",
            "filename": filename
        }

        # -----------------------------------------
        # 1. Select the document loader
        # -----------------------------------------

        if source_url:

            # Load webpage content directly from the URL
            loader = WebBaseLoader(source_url)
            extension = "url"

        else:

            if not content:
                raise ValueError(
                    "File content is missing."
                )

            extension = os.path.splitext(filename)[1].lower()

            if extension not in {".pdf", ".csv", ".txt"}:
                raise ValueError(
                    "Unsupported file type. "
                    "Only PDF, CSV, and TXT are supported."
                )

            # Create a temporary file for uploaded content
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temp_file:

                temp_file.write(content)
                temp_path = temp_file.name

            # Select file loader
            if extension == ".pdf":
                loader = PyPDFLoader(temp_path)

            elif extension == ".csv":
                loader = CSVLoader(temp_path)

            else:
                loader = TextLoader(temp_path)

        # -----------------------------------------
        # 2. Load document
        # -----------------------------------------

        docs = loader.load()
        print("Total documents loaded:", len(docs))

        if not docs:
            raise ValueError(
                "No content could be extracted from the source."
            )

        # -----------------------------------------
        # 3. Split document
        # -----------------------------------------

        chunks = splitting_docs(docs)
        print("Total chunks, :", len(chunks))

        if not chunks:
            raise ValueError(
                "Document splitting produced no chunks."
            )

        # -----------------------------------------
        # 4. Generate embeddings
        # -----------------------------------------

        embeddings = embed_docs()

        # -----------------------------------------
        # 5. Create FAISS retriever
        # -----------------------------------------

        retriever = storing_vector_and_retriever(
            chunks,
            embeddings,
            extension
        )

        retriever_store[job_id] = retriever

        # -----------------------------------------
        # 6. Create RAG chain
        # -----------------------------------------

        chain = prompts_and_chains(
            llm,
            retriever
        )

        chain_store[job_id] = chain

        # -----------------------------------------
        # 7. Initialize chat history
        # -----------------------------------------

        chat_history_store[job_id] = []

        # -----------------------------------------
        # 8. Mark job as completed
        # -----------------------------------------

        job_status[job_id] = {
            "status": "completed",
            "filename": filename,
            "chunks": len(chunks),
            "source_type": "url" if source_url else "file"
        }

    except Exception as error:

        job_status[job_id] = {
            "status": "failed",
            "filename": filename,
            "error": str(error)
        }

    finally:

        # Remove temporary uploaded file.
        # WebBaseLoader does not create this file.
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)