# DocuMind AI

**DocuMind AI** is a full-stack document question-answering application that allows users to upload documents or provide website URLs and ask questions using Retrieval-Augmented Generation (RAG).

The application combines **Streamlit**, **FastAPI**, **LangChain**, **LLMs**, and **vector similarity search** to provide conversational answers based on the content of uploaded documents.

## Features

* Upload and process PDF, CSV, and TXT files.
* Ingest content from website URLs.
* Convert documents into manageable text chunks.
* Generate embeddings for document chunks.
* Store and retrieve relevant information using vector similarity search.
* Ask natural-language questions about uploaded documents.
* Generate answers using a Large Language Model.
* Maintain conversational question-answering functionality.
* Process documents through background jobs.
* Track document-processing status.
* Provide REST API endpoints through FastAPI.
* Apply basic API rate limiting.
* Support deployment of the frontend and backend as separate services.

## Technology Stack

### Frontend

* Streamlit
* Python
* Requests
* Environment-based API configuration

### Backend

* FastAPI
* Uvicorn
* Pydantic
* Python

### AI and Retrieval

* LangChain
* Large Language Models
* Embedding models
* Retrieval-Augmented Generation
* Vector similarity search

### Supported Input Types

* PDF documents
* CSV files
* TXT files
* Website URLs

## Project Architecture

```text
DocuMindAI/
│
├── app.py                         # Streamlit frontend
│
├── api/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── schemas.py                 # Request and response schemas
│   └── rate_limiter.py             # API rate limiting
│
├── services/
│   ├── __init__.py
│   ├── ingestion_service.py       # Document ingestion and processing
│   └── ...
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py                 # Streamlit sidebar components
│   └── ...
│
├── utils/
│   ├── __init__.py
│   ├── vectorStoreAndRetriever.py # Vector store and retriever logic
│   └── ...
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment configuration
├── .gitignore
└── README.md
```

## Application Workflow

```text
User uploads a document or enters a website URL
                    │
                    ▼
          Document ingestion
                    │
                    ▼
       Text extraction and cleaning
                    │
                    ▼
             Text chunking
                    │
                    ▼
          Embedding generation
                    │
                    ▼
             Vector storage
                    │
                    ▼
        Similarity-based retrieval
                    │
                    ▼
         Relevant context selection
                    │
                    ▼
       LLM-based answer generation
                    │
                    ▼
          Answer shown to user
```

## Requirements

Before running the project, install the following:

* Python 3.10 or later
* Git
* A configured LLM or OpenRouter API key
* Internet access for model and embedding requests

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aafreen-Siddiqui/DocuMindAI-FullStack.git
cd DocuMindAI
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key

FROM_EMAIL=your_sender_email
TO_EMAIL=recipient_email
EMAIL_SUBJECT=Document Processing Notification
```

> Do not commit your `.env` file or any API keys to GitHub. Keep all secrets private.

If the project uses additional variables, add them to your local `.env` file according to the implementation.

## Running the Application Locally

The project contains a Streamlit frontend and a FastAPI backend.

### 1. Start the FastAPI backend

From the project root, run:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### 2. Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run app.py
```

The Streamlit application will normally be available at:

```text
http://localhost:8501
```

## Backend API Endpoints

| Method | Endpoint                     | Description                                         |
| ------ | ---------------------------- | --------------------------------------------------- |
| `GET`  | `/`                          | Returns a basic API response                        |
| `GET`  | `/health`                    | Checks backend health                               |
| `POST` | `/documents/upload`          | Uploads and processes a document                    |
| `GET`  | `/documents/status/{job_id}` | Checks document-processing status                   |
| `POST` | `/questions/ask`             | Sends a question to the document-questioning system |

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### API Documentation

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

This page provides an interactive interface for testing the available API endpoints.

## Configuration for Deployment

When the frontend and backend are deployed separately, the Streamlit frontend should use the deployed FastAPI URL instead of the local backend URL.

Example:

```python
import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)
```

For deployment, configure the frontend with the public backend URL:

```text
https://your-backend-service.onrender.com
```

The API URL should be stored as an environment variable or Streamlit secret rather than being hardcoded.

## Deployment

### Streamlit Frontend

The Streamlit frontend can be deployed using Streamlit Community Cloud.

General deployment steps:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Select the GitHub repository.
4. Select the `main` branch.
5. Set the main file to:

```text
app.py
```

6. Add the required secrets and environment variables.
7. Deploy the application.

### FastAPI Backend

The FastAPI backend can be deployed using a platform such as Render.

Recommended build command:

```bash
pip install -r requirements.txt
```

Recommended start command:

```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

After deployment, copy the backend URL and configure it in the Streamlit frontend.

## Important Notes and Limitations

* The application requires valid API credentials for the configured AI services.
* API keys must not be exposed in source code or committed to GitHub.
* Retrieved document chunks determine the context available to the language model.
* For large documents, the system may retrieve only the most relevant chunks rather than the entire document.
* For structured CSV analysis involving exact totals, averages, or complete-row calculations, a dedicated data-analysis workflow may be more suitable than similarity-based retrieval alone.
* Backend and frontend services must be running and correctly configured for the complete application to work locally.
* The deployed frontend must point to the public backend URL instead of `localhost`.

## Security Considerations

* Store secrets in environment variables or deployment-platform secret managers.
* Never upload `.env` files to GitHub.
* Use `.gitignore` to exclude credentials, virtual environments, cache files, and generated data.
* Configure appropriate API rate limits.
* Do not expose private documents or sensitive information through public deployments.
* Review uploaded documents before sharing the application publicly.

## Future Improvements

* Add user authentication and authorization.
* Support additional document formats.
* Improve retrieval quality using hybrid search or reranking.
* Add document deletion and management features.
* Add persistent vector-database storage.
* Improve exact numerical analysis for CSV files.
* Add automated testing.
* Add monitoring and logging.
* Improve error handling and user feedback.
* Support multiple users and separate document collections.

## Author

**Afreen Siddiqui**

## License

This project is intended for educational, demonstration, and portfolio purposes. Add an appropriate open-source license if you plan to distribute or reuse the project publicly.
