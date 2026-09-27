# ClauseGuard: Legal PDF Auditor & Risk Agent

**ClauseGuard** is an AI-powered legal document analysis tool designed to audit legal PDFs, extract obligations, detect risks, and answer document-specific queries. Built on FastAPI, Streamlit, ChromaDB, and LangChain, it utilizes a multi-model fallback strategy hosted on Groq to enforce strict context-bound retrieval and prevent legal hallucinations.

---

## Key Features

- **Strict Document Grounding:** Answers are generated *strictly* using content retrieved from the uploaded legal document.
- **Resilient AI Pipeline:** Uses a 4-tier model fallback chain to guarantee high availability and low latency via Groq.
- **RAG Architecture:** Leverages ChromaDB for vector storage, persistent indexing, and semantic chunk retrieval.
- **Stateful Audit Agent:** Uses LangGraph/LangChain checkpointers to support multi-turn conversational threads tied to specific document IDs.
- **Interactive Dashboard:** Includes a Streamlit frontend for uploading documents and chatting with the auditor agent in real-time.

---

## Project Structure

```text
ClauseGuard/
│
├── chroma_db/             # Persistent ChromaDB vector store
├── db_setup/              # Database & LangChain checkpointer setup
├── model/                 # AI agent, fallback chains, and inference logic
├── Schema/                # Pydantic schemas for request validation
├── VectorDB/              # Document loading, chunking, and embedding workflows
│   ├── pdf_loader.py
│   ├── chunking.py
│   └── vector_embedding.py
│
└── src/
    ├── backend/           # FastAPI application (app.py)
    └── frontend/          # Streamlit user interface (index.py)
```

---

## AI Agent Architecture & Models

ClauseGuard executes agentic workflows through a strict system prompt and a tool-augmented fallback chain on Groq:

| Tier | Model | Role |
| :--- | :--- | :--- |
| **Primary** | `openai/gpt-oss-120b` | Primary analysis & complex reasoning |
| **Fallback 1** | `openai/gpt-oss-20b` | Low-latency backup for standard inference |
| **Fallback 2** | `qwen/qwen3.8-27b` | High-accuracy multilingual/structured backup |
| **Fallback 3** | `openai/gpt-oss-safeguard-20b` | Final safety-focused fallback layer |

### Core Guardrails
- **Tool-First Retrieval:** The agent is forced to call the `search_document` retriever tool before producing any answer.
- **Anti-Hallucination:** Answers rely solely on retrieved document chunks. External general knowledge generation is strictly prohibited by system instructions.

---

## API Documentation

The FastAPI backend exposes the following endpoints:

| Endpoint | Method | Input | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | None | Welcome message |
| `/health` | `GET` | None | Server health status check |
| `/document` | `POST` | `file` (PDF), `thread_id` (UUID) | Ingests, chunks, embeds, and stores the PDF in ChromaDB |
| `/invoke` | `POST` | `JSON` (`user_msg`, `thread_id`) | Queries the legal audit agent with conversational memory |

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- A Groq API Key

### 2. Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/ClauseGuard.git
cd ClauseGuard
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `config.py` file in the root directory (or use environment variables) containing your Groq API key:

```python
# config.py
api_key = "your_groq_api_key_here"
```

### 4. Running the Backend

Start the FastAPI server from the project root:

```bash
uvicorn src.backend.app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. You can test endpoints via the interactive Swagger docs at `http://localhost:8000/docs`.

### 5. Running the Frontend

Launch the Streamlit user interface:

```bash
streamlit run src/frontend/index.py
```

The UI will open automatically in your browser at `http://localhost:8501`.

---

## How It Works

1. **Upload Phase:** A user uploads a legal agreement through the Streamlit interface. The file is sent to `/document` with a generated `thread_id`.
2. **Indexing Phase:** PyMuPDF/PDF extractors parse the document, split it into chunks, embed the text, and store it in ChromaDB.
3. **Audit Phase:** The user prompts the agent via `/invoke`. The agent retrieves context using `search_document`, applies strict guardrails, and returns precise, jargon-free legal risk summaries.