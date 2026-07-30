# 📄 DocuMind AI

**DocuMind AI** is an Intelligent Enterprise Knowledge Assistant built using **Retrieval-Augmented Generation (RAG)**. It enables users to upload documents or provide a website URL and ask questions in natural language. The application retrieves relevant information from the knowledge base and generates context-aware responses using a Large Language Model.

---

## 🚀 Features

- 📄 Chat with PDF documents
- 📃 Chat with TXT files
- 📊 Chat with CSV files (supports up to 2000 rows)
- 🌐 Chat with website content using URL
- 💬 Conversational chat with history
- 🧠 History-aware retrieval for context-aware responses
- ⚡ Fast semantic search using FAISS
- 🔍 Retrieval-Augmented Generation (RAG)
- 🎯 Modular architecture
- 🚀 Cached document processing for better performance
- 🎨 Clean Streamlit interface

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### LLM
- Groq (Llama 3.3 70B Versatile)

### Framework
- LangChain

### Vector Database
- FAISS

### Embedding Model
- HuggingFace Embeddings

### Document Loaders
- PyPDFLoader
- CSVLoader
- TextLoader
- WebBaseLoader

---

## 📂 Project Structure

```text
DocuMindAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── components/
│   └── sidebar.py
│
├── utils/
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vectorStoreAndRetriever.py
│   ├── prompts.py
│   └── rag_chain.py
│
└── assets/
```

---

## 🧠 How It Works

1. Upload a document (PDF, TXT, CSV) or enter a website URL.
2. The document is loaded using the appropriate LangChain Loader.
3. The content is split into smaller chunks.
4. HuggingFace Embeddings convert chunks into vector representations.
5. FAISS stores the embeddings for semantic similarity search.
6. A History-Aware Retriever retrieves the most relevant context.
7. The retrieved context is passed to the LLM through a QA prompt.
8. The LLM generates an accurate and context-aware response.

---

## 🔄 RAG Pipeline

```text
User Input
      │
      ▼
Document Loader
      │
      ▼
Text Splitter
      │
      ▼
Embeddings
      │
      ▼
FAISS Vector Store
      │
      ▼
History-Aware Retriever
      │
      ▼
Question Answering Chain
      │
      ▼
Groq LLM
      │
      ▼
Response
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/DocuMindAI.git
```

Move into the project

```bash
cd DocuMindAI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
GROQ_API_KEY=your_api_key
```

Run the application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### Home Page

(Add Screenshot Here)

### Chat Interface

(Add Screenshot Here)

---

## 🎯 Future Improvements

- Multiple document upload
- Source citations
- Metadata filtering
- Hybrid Search
- MultiQuery Retriever
- Contextual Compression Retriever
- Streaming responses
- Deployment on Streamlit Cloud

---

## 👩‍💻 Author

**Afreen Siddiqui**

LinkedIn: https://www.linkedin.com/in/afreen-siddiqui-344419249/



---

## ⭐ If you found this project useful, consider giving it a star.