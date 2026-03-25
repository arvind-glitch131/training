# 📚 Multi-Doc RAG with Explicit Source Citations

A high-precision Retrieval-Augmented Generation (RAG) system built with **LangChain v0.3**, **FAISS**, and **Groq**. This system is designed to answer questions across multiple documents while providing explicit inline citations and page references, ensuring zero hallucinations.

---

## 🏗️ Advanced Architecture

This project solves the "Source Blending" problem by using **Metadata Prefix Tagging**.

### 1. Ingestion Engine (`ingestion.py`)
* **Multi-Format Support**: Automatically detects and loads both `.pdf` and `.txt` files from a local directory.  
* **Recursive Chunking**: Splits documents into 1,000-character blocks while strictly preserving metadata (filename and page number).  
* **Local Embedding**: Uses `all-MiniLM-L6-v2` locally via your CPU to convert text into mathematical vectors.  

### 2. Citation Logic (`main.py`)
* **Source Tagging**: Before the LLM sees the retrieved text, each chunk is "wrapped" in a header: `[SOURCE: filename.pdf]`.  
* **Inline Attribution**: The prompt forces the LLM to use these tags to cite its claims (e.g., "The dough must ferment for 12 hours [bread_recipe.pdf]").  
* **Deduplicated References**: A clean footer is generated that lists every unique file and page used to construct the answer.  

---

## 🔄 The RAG Flow (Step-by-Step)

1. **Search**: The system finds the 3 most relevant text snippets across all files in the `data/` folder.  
2. **Tagging**: The script extracts the filename from the metadata and attaches it to the top of each snippet.  
3. **Prompting**: The LLM receives a "Context" block where every paragraph is labeled by its source.  
4. **Verification**: The LLM is instructed to say "I don't know" if the answer isn't in those labeled paragraphs.  
5. **Output**: You receive a factual answer with bracketed citations and a summary of sources.  

---

## 🛠️ Tech Stack

* **Orchestration**: LangChain v0.3 (LCEL)  
* **Inference**: Groq Cloud (Llama-3.3-70b-versatile)  
* **Vector DB**: FAISS (Facebook AI Similarity Search)  
* **Embeddings**: HuggingFace `sentence-transformers` (Local CPU)  
* **Environment**: Python 3.12+ & Dotenv  

---

## 🚀 Getting Started

### 1. Installation

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. File Setup

1. Create a folder named `data/` in the project root.  
2. Drop your `.pdf` and `.txt` files into the `data/` folder.  
3. Create a `.env` file and add your key:

    GROQ_API_KEY=gsk_your_key_here

---

### 3. Run the System

    python main.py

---

## 📂 Project Modules

| Module | Responsibility |
| :--- | :--- |
| `ingestion.py` | Scans folders, parses multiple file types, and creates the FAISS index. |
| `main.py` | Handles retrieval, source-prefixing, and the interactive chat loop. |
| `prompts.py` | Contains the strict system instructions for citations and "I don't know" logic. |
| `requirements.txt` | Lists the specific versions of LangChain, Groq, and FAISS. |

---

## 🎯 Key Capabilities

* **Explicit Attribution**: No more guessing which file the AI is quoting.  
* **Page-Level Accuracy**: Automatically calculates and displays PDF page numbers.  
* **Hybrid Processing**: High-speed cloud generation with completely private local indexing.  
* **Hallucination Guard**: Strict "No Answer Found" constraints prevent the AI from making up information.