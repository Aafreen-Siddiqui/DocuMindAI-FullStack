# DocuMind AI

DocuMind AI is a full-stack document question-answering application that allows users to upload documents and ask questions about their content using Large Language Models and Retrieval-Augmented Generation (RAG).

The application combines a Streamlit frontend, FastAPI backend, document processing, vector search, and LLM-based response generation.

---

## Important Links

- **GitHub Repository:**  
  https://github.com/Aafreen-Siddiqui/DocuMindAI-FullStack.git

- **Mandatory Explanations Document:**  
  https://drive.google.com/file/d/1o1GG4e19qrtHmaCapsgEzaF5QFzw4p9z/view?usp=sharing

- **System Architecture Diagram:**  
  https://drive.google.com/file/d/1MBaaoXqWZYcEQ1fXYQ93j0Sua-p1bsVa/view?usp=drive_link

> Make sure the Google Drive files are accessible using the permission **Anyone with the link can view**.

---

## Features

- Upload and process documents.
- Ask questions based on uploaded documents.
- Retrieve relevant document content using vector similarity search.
- Generate context-aware answers using Large Language Models.
- Streamlit-based interactive frontend.
- FastAPI-based backend.
- REST API endpoints for document processing and question answering.
- Modular project structure for future improvements and deployment.
---

## Technology Stack

### Frontend

- Streamlit
- Python

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Artificial Intelligence and Machine Learning

- Large Language Models
- Retrieval-Augmented Generation
- Embeddings
- Vector similarity search
- LangChain and related components

### Document Processing

- PDF/document text extraction
- Text chunking
- Document preprocessing

### Configuration and Environment

- Python-dotenv
- Environment variables
- API keys for external AI services

---

## Project Structure

```text
DocuMindAI-FullStack/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── ...
│
├── frontend/
│   ├── app.py
│   └── ...
│
├── data/
│   └── ...
│
├── requirements.txt
├── .env.example
├── README.md
└── ...
```

> The exact folder and file names may vary depending on the current implementation of the project.

---

## Prerequisites

Before running the project, install the following:

- Python 3.10 or later
- Git
- A virtual environment
- Required API keys
- Internet connection for accessing external AI services

Python 3.11 is recommended if you experience compatibility issues with newer Python versions.

---

## Clone the Repository

```bash
git clone https://github.com/Aafreen-Siddiqui/DocuMindAI-FullStack.git
cd DocuMindAI-FullStack
```

---

## Create and Activate a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root directory.

Example:

```env
GROQ_API_KEY=your_groq_api_key
hugging_face_API_KEY=your_hugging_face_api_key



> Only add the environment variables required by your current implementation. Never upload your actual API keys or passwords to GitHub.

---

## Running the Application Locally

The application consists of two main components:

1. FastAPI backend
2. Streamlit frontend

Run both components in separate terminals.

---

### Step 1: Start the FastAPI Backend

From the project root directory, run:

```bash
uvicorn backend.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

### Step 2: Start the Streamlit Frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

The Streamlit frontend will normally be available at:

```text
http://localhost:8501
```

> Update the commands above if your actual backend or frontend entry-point files have different names.

---

## Application Workflow

The general workflow of the application is:

```text
User uploads a document
          │
          ▼
Document text is extracted
          │
          ▼
Text is divided into smaller chunks
          │
          ▼
Embeddings are generated
          │
          ▼
Document chunks are stored or indexed
          │
          ▼
User asks a question
          │
          ▼
Relevant document chunks are retrieved
          │
          ▼
Retrieved context is sent to the LLM
          │
          ▼
The generated answer is displayed to the user
```

---

## API Endpoints

The backend exposes API endpoints for handling application functionality.

Commonly used endpoints may include:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the backend is running |
| GET | `/docs` | Opens the interactive FastAPI documentation |
| POST | `/upload` | Uploads and processes a document |
| POST | `/ask` | Sends a question to the document-question-answering system |

> The exact endpoints depend on the current implementation. Open `/docs` after starting the backend to view the available and updated endpoints.

---

## Deployment Status

The project is currently configured to run locally.

At present, the application has **not been deployed to a public hosting platform**. The frontend and backend can be started locally by following the instructions in the **Running the Application Locally** section.

### Local Application URLs

- **Streamlit frontend:** `http://localhost:8501`
- **FastAPI backend:** `http://127.0.0.1:8000`
- **FastAPI documentation:** `http://127.0.0.1:8000/docs`

Deployment to platforms such as Streamlit Community Cloud or Render may be considered in the future.

---

## Security Considerations

- Do not commit the `.env` file to GitHub.
- Do not expose API keys in source code.
- Use `.env.example` to document required environment variables.
- Add `.env` to `.gitignore`.
- Validate uploaded files before processing them.
- Apply suitable file-size and file-type restrictions.
- Avoid logging sensitive user information.

---

## Limitations

- The application currently requires valid API credentials for external AI services.
- Response quality depends on the quality of the uploaded documents and the selected language model.
- Very large documents may require additional processing time.
- The application is currently intended for local execution.
- Public deployment and production-level monitoring have not yet been implemented.

---

## Future Improvements

- Deploy the frontend and backend to cloud platforms.
- Add user authentication and authorization.
- Add support for more document formats.
- Improve document processing speed.
- Add persistent vector database storage.
- Add conversation history.
- Improve error handling and logging.
- Add automated testing.
- Add production monitoring.
- Improve frontend design and user experience.

---

## Troubleshooting

### Dependency Installation Issues

Make sure the virtual environment is activated before installing dependencies:

```bash
pip install -r requirements.txt
```

### API Key Error

Check whether the required API keys are correctly added to the `.env` file.

### Backend Connection Error

Make sure the FastAPI backend is running before using the frontend.

### Frontend Cannot Access Backend

Check the backend URL configured in the frontend code and confirm that the backend is running at the expected address.

### Port Already in Use

You can start the backend on another port:

```bash
uvicorn backend.main:app --reload --port 8001
```

---

## Author

**Aafreen Siddiqui**

GitHub:  
https://github.com/Aafreen-Siddiqui