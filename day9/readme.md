# Research Assistant Agent (ReAct Pattern)

An autonomous AI agent built with LangChain (v0.3+) and Groq that researches a given topic, synthesizes a summary, and saves the output to a local file.

---

## 🚀 Features

* **Autonomous Reasoning**: Implements the ReAct (Reasoning + Acting) pattern to decide when to search and when to write.  
* **High-Speed Inference**: Powered by Groq (Llama 3.3) for near-instant "thought" cycles.  
* **Real-time Web Access**: Uses the Tavily API to fetch cleaned, LLM-ready search results.  
* **Physical Action**: Includes a custom `file_writer` tool to persist data to the disk.  

---

## 🛠️ Tech Stack

* **LLM**: llama-3.3-70b-versatile (via Groq)  
* **Framework**: langchain, langchain-classic, langchain-community  
* **Search Engine**: Tavily AI  
* **Environment**: Python 3.14+  

---

## 📂 Project Structure

    research_agent/
    ├── agent.py          # Main Agent logic & ReAct loop
    ├── tools.py          # Custom File Writer tool definition
    ├── .env              # API Keys (Groq & Tavily)
    ├── requirements.txt  # Dependencies
    └── research_output/  # Automatically generated folder for summaries

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

    pip install -r requirements.txt

### 2. Configure Environment

Create a `.env` file in the root directory:

    GROQ_API_KEY=your_groq_key_here
    TAVILY_API_KEY=your_tavily_key_here

### 3. Run the Agent

    python agent.py

---

## 🧠 Logic Flow: The ReAct Pattern

The agent follows a multi-step execution loop:

1. **Input**: User provides a research topic.  
2. **Thought**: The Agent analyzes if it has enough internal knowledge (it usually doesn't).  
3. **Action**: It invokes the TavilySearchResults tool.  
4. **Observation**: It reads and filters the web data.  
5. **Thought**: It synthesizes the key points and prepares a filename.  
6. **Action**: It invokes the `file_writer` tool.  
7. **Final Response**: Confirms the file path to the user.  

---