# Context-Aware Chatbot (LangChain + Groq)

## Introduction
This project is a multi-turn AI chatbot built using LangChain v0.3, designed to maintain conversation history across interactions.

It is powered by Groq's Llama-3.3 model, enabling fast, intelligent, and context-aware responses while remembering previous user inputs within a session.

---

## Core Architecture

The system is built using three main components:

### 1. Modular Prompt
- Uses MessagesPlaceholder to dynamically inject conversation history
- Ensures the model receives both past and current context

### 2. LCEL Chain (LangChain Expression Language)
- Pipes the prompt directly into the LLM
- Enables clean, composable, and efficient chaining

### 3. Session-Based Memory
- Maintains chat history using a unique session ID
- Stores conversations in an internal dictionary for retrieval

---

## How It Works

1. User Input  
   The user sends a message to the chatbot

2. History Fetching  
   The system retrieves previous messages using the session ID

3. Context Injection  
   Past messages and current input are combined into a single prompt

4. LLM Processing  
   Groq API processes the full context and generates a response

5. History Update  
   The new response is stored for future interactions

---

## Tech Stack

- Framework: LangChain v0.3  
- LLM Provider: Groq Cloud  
- Model: llama-3.3-70b-versatile  
- Environment: Python Dotenv  
- Memory Management: LangChain Community ChatMessageHistory  

---

## Setup Instructions

### 1. Create Virtual Environment
python -m venv venv
### 2. Activate Environment
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
### 3. Install Dependencies
pip install langchain-groq langchain-community python-dotenv
### 4. Configure Environment Variables

Create a .env file and add:

GROQ_API_KEY=your_api_key_here
### 5. Run the Application
python main.py

### Key Features
- Remembers user details across conversations
- Maintains multi-turn context seamlessly
- High-speed inference using Groq LPU
- Stateless design for better scalability
- Supports multiple independent chat sessions