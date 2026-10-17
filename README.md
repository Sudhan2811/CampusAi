# CampusAI — AI-Powered Campus Assistant

CampusAI is an AI-powered assistant designed to answer campus-related questions using Retrieval-Augmented Generation (RAG). It combines a FastAPI backend, FAISS-based semantic search, and Amazon Bedrock to retrieve relevant information and generate context-aware responses.

## Features

- **Retrieval-Augmented Generation (RAG):** Retrieves relevant text chunks from campus documents before generating answers.
- **Semantic Search:** Uses Sentence Transformers and FAISS for vector-based document retrieval.
- **LLM Integration:** Uses Amazon Bedrock to generate natural-language responses.
- **Source Traceability:** Returns source document names and retrieval similarity scores.
- **Answerability Testing:** Includes an evaluation script to test whether expected evidence appears in retrieved context.
- **Tool Integration:** Supports assistant tools for calculations, opening websites and VS Code, date/time, weather, forecasts, and music searches.
- **Voice Interaction:** Supports voice input and spoken responses through the frontend.
- **Safety Checks:** Includes basic request filtering and restricted tool execution.

## Technology Stack

- Python
- FastAPI
- Amazon Bedrock
- FAISS
- Sentence Transformers (`all-MiniLM-L6-v2`)
- NumPy
- HTML, CSS, and JavaScript
- Web Speech API

## Architecture

1. **Document ingestion:** Campus documents are split into text chunks.
2. **Embedding generation:** Sentence Transformers converts chunks into vector embeddings.
3. **Vector indexing:** FAISS stores the embeddings for similarity search.
4. **Retrieval:** A user question is embedded and matched against indexed chunks.
5. **Answer generation:** Retrieved context is passed to an Amazon Bedrock model.
6. **Response:** CampusAI returns the generated answer and source information.

## Project Structure

```text
mybot/
├── backend/       # FastAPI application and Bedrock integration
├── data/          # Source documents
├── frontend/      # User interface
├── rag/           # Retrieval, indexing, and evaluation
├── tests/         # Project tests
├── tools/         # Assistant tools
├── voice/         # Voice-related functionality
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Run

### Prerequisites

- Python 3.10 or a compatible version supported by your dependencies
- Git
- AWS credentials configured locally
- Access to the selected Amazon Bedrock model in your AWS region

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure AWS

Configure AWS credentials using your local AWS CLI profile or environment. Ensure the selected model is available and your AWS identity has permission to invoke it.

**Never commit AWS credentials, secret keys, or your `.env` file.**

### 5. Start the backend

```powershell
python -m uvicorn backend.main:app --reload
```

The API should be available at `http://127.0.0.1:8000`. API documentation is available at `/docs`.

### 6. Start the frontend

Open a second terminal from the project root:

```powershell
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500` in your browser.

### 7. Evaluate RAG retrieval

After the FAISS index and chunk files have been made available locally:

```powershell
python -m rag.evaluate_retriever
```

The evaluation script checks whether expected keywords appear in retrieved context. It is a basic retrieval test, not a comprehensive evaluation of answer correctness.

## Current Evaluation

The initial six-question evaluation on the included B.Tech registration notice found:

- Expected evidence for 4 out of 4 answerable questions in the top three retrieved chunks.
- No expected answer phrases for 2 unanswerable questions.
- Eight indexed chunks from one admission registration notice.

These results are from a small test set and should not be interpreted as a guarantee of overall answer accuracy.

## Limitations

- Retrieval quality depends on document coverage, chunking, and embedding similarity.
- Similarity scores do not guarantee factual correctness.
- The current keyword-based evaluation is limited.
- Safety filtering is a basic safeguard, not a guarantee against all unsafe actions.
- Amazon Bedrock usage may incur charges depending on the account and model.

## Future Improvements

- Expand the campus document collection.
- Improve retrieval evaluation and answer grounding.
- Add automated tests for API endpoints and tool execution.
- Improve source citations and error handling.
- Strengthen safety controls and deployment configuration.

## Author

Developed as a project to explore Large Language Models, Retrieval-Augmented Generation, semantic search, API development, and AI tool integration.
