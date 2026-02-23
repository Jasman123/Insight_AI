# 🤖 Insight AI

An intelligent, document-aware AI assistant powered by Retrieval-Augmented Generation (RAG). Insight AI lets you upload documents, build a searchable vector knowledge base, and have natural language conversations grounded in your own data — all wrapped in a clean Streamlit interface.

---

## ✨ Features

- 📄 **Document Ingestion** — Load and process documents from the `documents/` folder
- 🧠 **Vector Search** — Supports both **ChromaDB** (local) and **Pinecone** (cloud) as vector stores
- 🔗 **Graph-based Reasoning** — Uses a LangGraph-powered pipeline (`graph_model.py`) for structured, multi-step LLM reasoning
- 💬 **Conversational Interface** — Multi-page Streamlit app for a smooth chat experience
- 📑 **PDF Report Generation** — Export insights and responses as PDF documents
- 🐳 **Dockerized** — Fully containerized for easy deployment anywhere

---

## 🗂️ Project Structure

```
Insight_AI/
├── app.py                      # Main Streamlit application entry point
├── llm.py                      # LLM setup and configuration
├── retriever.py                # RAG retriever logic
├── graph_model.py              # LangGraph reasoning pipeline
├── build_vectore.py            # Build ChromaDB vector store
├── build_vectore_pinecone.py   # Build Pinecone vector store
├── generate_pdf.py             # PDF export functionality
├── pages/                      # Streamlit multi-page app views
├── chroma_db/                  # Local ChromaDB vector store
├── documents/                  # Source documents for ingestion
├── logs/                       # Application logs
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container configuration
└── .dockerignore / .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An OpenAI API key (or compatible LLM provider)
- *(Optional)* A Pinecone API key for cloud vector storage

### 1. Clone the Repository

```bash
git clone https://github.com/Jasman123/Insight_AI.git
cd Insight_AI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Documents

Place your source documents (PDFs, text files, etc.) inside the `documents/` folder.

### 4. Build the Vector Store

**Using ChromaDB (local):**
```bash
python build_vectore.py
```

**Using Pinecone (cloud):**
```bash
python build_vectore_pinecone.py
```

### 5. Run the App

```bash
streamlit run app.py
```

---

## 🐳 Running with Docker

```bash
# Build the image
docker build -t insight-ai .

# Run the container
docker run -p 8501:8501 insight-ai
```

Then visit `http://localhost:8501` in your browser.

---

## ⚙️ Configuration

Set the following environment variables before running:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `PINECONE_API_KEY` | Your Pinecone API key *(if using Pinecone)* |
| `PINECONE_ENV` | Your Pinecone environment *(if using Pinecone)* |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) |
| LLM Orchestration | [LangChain](https://www.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/) |
| Vector Store | [ChromaDB](https://www.trychroma.com/) / [Pinecone](https://www.pinecone.io/) |
| LLM | OpenAI GPT (configurable) |
| Containerization | Docker |

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

---

## 🙋‍♂️ Author

**Jasman** — [GitHub](https://github.com/Jasman123)
