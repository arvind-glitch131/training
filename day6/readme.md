# 📄 PDF-Based RAG System (Retrieval-Augmented Generation)

A modular RAG pipeline built with **LangChain v0.3**, **FAISS**, and **Groq**. This application allows users to upload a PDF document and ask questions based specifically on its content. The system uses local embeddings for privacy and speed, while leveraging Groq's LPU inference for high-performance generation.

## 🏗️ Architecture & Data Flow

This project implements a standard RAG architecture, splitting the process into two main phases: **Ingestion** and **Retrieval/Generation**.

### 1. The Ingestion Phase (Local)
* **Loading**: The `PyPDFLoader` converts the PDF into raw text documents.
* **Chunking**: `RecursiveCharacterTextSplitter` breaks long text into 1,000-character segments with a 200-character overlap to preserve semantic context.
* **Embedding**: Using `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`), text chunks are converted into 384-dimensional vectors locally on your CPU.
* **Vector Store**: `FAISS` (Facebook AI Similarity Search) indexes these vectors for near-instant mathematical retrieval.

### 2. The Retrieval & Generation Phase (Hybrid)
* **Query Vectorization**: Your question is converted into a vector using the same local embedding model.
* **Similarity Search**: FAISS identifies the top-K most relevant chunks from the PDF.
* **Contextual Prompting**: The retrieved chunks are injected into a modular prompt template as "Context."
* **LLM Generation**: The prompt is sent to the Groq Cloud (`Llama-3.3-70b`), which generates an answer based **only** on the provided context.

---

## 🔄 How It Works (Step-by-Step)

1. **User Input**: You provide a PDF file and ask a question.  
2. **Retrieval**: The system searches the local FAISS index to find text snippets that "match" the meaning of your question.  
3. **Augmentation**: The snippets are added to a hidden instruction: *"Answer this question using ONLY the following text..."*  
4. **Generation**: Groq processes the instruction and returns a concise, factual answer.  

---

## 🛠️ Tech Stack

* **Framework**: LangChain v0.3 (LCEL)  
* **LLM**: Groq Cloud (Llama-3.3-70b-versatile)  
* **Vector Database**: FAISS-cpu  
* **Embeddings**: HuggingFace (Local)  
* **PDF Parsing**: PyPDF  
* **Text Splitting**: LangChain Text Splitters  

---

## 🚀 Getting Started

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # macOS/Linux

# Install required packages
pip install langchain-groq langchain-huggingface langchain-community langchain-text-splitters pypdf faiss-cpu python-dotenv 
```

### 2. Configuration

Create a `.env` file in the root directory:

    GROQ_API_KEY=gsk_your_actual_api_key_here

### 3. Usage

1. Place your PDF in the project directory (e.g., `document.pdf`).  
2. Update the hardcoded path in `main.py` if necessary.  
3. Run the application:

    python main.py

---

## 📂 Project Structure

| File | Responsibility |
| :--- | :--- |
| `main.py` | Coordinates the LCEL chain, retriever, and user input loop. |
| `ingestion.py` | Handles PDF loading, chunking, and FAISS index creation. |
| `prompts.py` | Defines the RAG-specific system instructions. |
| `.env` | Securely stores the Groq API credentials. |

---

## 🎯 Key Features

* **Local Processing**: Embeddings and Vector Search happen on your machine, ensuring data privacy for the majority of the process.  
* **Contextual Accuracy**: Reduces LLM hallucinations by forcing the model to answer based on document evidence.  
* **Hybrid Efficiency**: Combines local CPU-based vector search with cloud-based GPU-speed generation.