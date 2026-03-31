# Stateful Finance Assistant (Model Context Protocol)

This project demonstrates a high-level integration of an LLM with a Stateful MCP Server. Unlike standard API tools, this system maintains an internal "source of truth" (Transaction History) within the server process, allowing for complex, multi-turn financial tracking.

---

## 🚀 Key Features

* **Server-Side Persistence**: The MCP Server maintains a running history of transactions (`buy_price`, `sell_price`, `item_name`) independent of the LLM's context window.  
* **Multi-Tool Discovery**: The agent dynamically discovers and invokes two distinct tools: `record_transaction` and `get_final_summary`.  
* **Standardized Protocol**: Built using the official MCP SDK (2026 Standards), utilizing JSON-RPC over stdio transport.  
* **Interactive AI Loop**: A persistent client session that allows the user to record multiple items before generating a final audit report.  

---

## 🏗️ Architecture

The system is decoupled into two primary layers:

* **The Service Layer (`server.py`)**: Acts as the "Database and Logic" engine. It calculates profits/losses and stores them in a local memory list.  
* **The Host Layer (`client.py`)**: Acts as the "Intelligence" engine. It manages the user interface and uses Groq (Llama 3.3) to interpret the raw data coming from the server.  

---

## 🛠️ Tech Stack

* **Language**: Python 3.14  
* **Protocol**: mcp (Model Context Protocol)  
* **LLM**: llama-3.3-70b-versatile (via Groq)  
* **Async Framework**: asyncio & anyio (TaskGroups)  

---

## 📂 Project Structure

    day11_mcp_stateful/
    ├── server.py      # Stateful MCP Server with internal memory
    ├── client.py      # Interactive Agent (The Host)
    ├── .env           # Groq API Key
    └── requirements.txt

---

## 🔄 Logic Flow

1. **Handshake**: The Client launches the Server and performs an initialize handshake to exchange capabilities.  
2. **Recording**: User inputs transaction details. The Client sends this as a structured JSON-RPC call to the Server.  
3. **Storage**: The Server updates its `transaction_history` and returns a confirmation.  
4. **Summary**: When requested, the Server iterates through its history, calculates the net profit/loss, and sends the final figure to the Client.  
5. **Synthesis**: The LLM takes the raw net figure and drafts a professional concluding report.  

---

## ⚙️ Setup & Execution

### 1. Install Dependencies

    pip install mcp langchain-groq python-dotenv

### 2. Set API Key

Ensure `GROQ_API_KEY` is set in your `.env` file:

    GROQ_API_KEY=your_key_here

### 3. Run the Application

    python client.py

---

## 🧩 Reflection on the "Connection Closed" Fix

During development, we encountered a `TypeError` in `Server.get_capabilities()`. This was resolved by explicitly passing:

    experimental_capabilities={}

during server initialization — a requirement in the latest 2026 SDK updates for Python 3.14 compatibility.

---