import streamlit as st
from components.sidebar import show_sidebar
from utils.loader import load_document
from utils.splitter import splitting_docs
from utils.embeddings import embed_docs
from utils.vectorStoreAndRetriever import storing_vector_and_retriever
from utils.rag_chain import generate_response, prompts_and_chains
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import time
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="DocuMind AI")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

document = show_sidebar()
if document is None:
    current_source = None
elif isinstance(document, str):
    current_source = document
else:
    current_source = document.name

# ---------------- Session State ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_file" not in st.session_state:
    st.session_state.current_file = None
    


# ---------------- Build RAG only once per file ----------------

@st.cache_resource
def build_chain(document):
    start = time.time()
    docs = load_document(document)
    print("Loading:", time.time() - start)
    start = time.time()
    chunks = splitting_docs(docs)
    print("Splitting:", time.time() - start)
    start = time.time()
    embeddings = embed_docs()
    retriever = storing_vector_and_retriever(chunks, embeddings)
    print("Embedding + FAISS:", time.time() - start)
    
    return prompts_and_chains(llm, retriever)


# ---------------- Reset history on new upload ----------------

if document:

    if st.session_state.current_file != current_source:
        st.session_state.current_file = current_source
        st.session_state.chat_history = []

        st.toast("Document uploaded successfully!", icon="📄")
        try:

            with st.spinner("Processing document..."):
                chain = build_chain(document)
            st.toast("Knowledge base is ready!", icon="🎉")
        except Exception as e:
            st.error(str(e))
            st.stop()

    else:
        try:
            chain = build_chain(document)
        except Exception as e:
            st.error(str(e))
            st.stop()


query = st.chat_input("Ask anything about your documents...")

if not query:
    st.title("DocuMind AI")
    st.subheader("Intelligent Enterprise Knowledge Assistant")

    st.info("""
👋 **Welcome to DocuMind AI!**

Upload a document and start chatting with it.
""")


if document and query:

    response = generate_response(
        chain,
        query,
        st.session_state.chat_history
    )
    print("Response : ",response)
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
           
            with st.chat_message("user"):
                    st.write(message.content)

        elif isinstance(message, AIMessage):
            
            with st.chat_message("assistant"):
                st.write(message.content)
                