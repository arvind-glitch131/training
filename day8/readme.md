# 🤖 Modular Tool-Using AI Agent (ReAct)

A lightweight, modular AI agent built from scratch using **Python** and **Groq**. This agent doesn't just "chat"—it thinks, decides which tools to use, executes them, and observes the results to provide an accurate final answer.

---

## 🚀 The Problem Statement

Build an AI agent capable of using external tools (Calculator, Clock, etc.) to solve queries that a standard LLM might struggle with (like real-time math or current time), without using hardcoded "if-else" logic for tool selection.

---

## 🛠️ Architecture & Flow

The agent follows the **ReAct (Reasoning + Acting)** framework. Instead of the developer telling the AI when to use a tool, the AI identifies the need itself based on the tool descriptions provided in the system prompt.

### The Execution Loop:

1. **Input:** User asks a question (e.g., "What is the current hour times 5?").  
2. **Thought:** The LLM reasons about the steps needed.  
3. **Action:** The LLM selects a tool from the **Tool Registry**.  
4. **Action Input:** The LLM provides the necessary parameters.  
5. **Observation:** Our Python script executes the tool and feeds the result back to the LLM.  
6. **Final Answer:** Once the LLM has enough information, it generates the final response.  

---

## 📂 Project Structure

* `agent.py`: The "Orchestrator" containing the ReAct loop and Groq integration.  
* `tools.py`: The **Modular Tool Registry**. Functions are defined here independently.  
* `prompts.py`: Contains the system instructions that define the "Action/Observation" protocol.  
* `.env`: Stores the `GROQ_API_KEY`.  

---

## ⚙️ Features

* **Zero Hardcoding:** Tool selection is handled entirely by the LLM's reasoning.  
* **Modular Design:** New tools can be added to `tools.py` without changing the core agent logic.  
* **Groq Powered:** Utilizes Llama 3 (via Groq) for lightning-fast inference loops.  
* **Transparent Logic:** The terminal displays the "Internal Monologue" (Thought/Action/Observation) so you can see the agent's "brain" working.  

---

## 🚦 Getting Started

### 1. Clone & Setup venv

```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install groq python-dotenv
```

### 2. Add API Key

Create a `.env` file and add:

    GROQ_API_KEY=your_key_here

---

### 3. Run the Agent

    python agent.py

---

## 📝 Example Trace

**User:** "What is the current year plus 10?"

**AI Internal Logic:**

> **Thought:** I need to get the current date to find the year, then add 10.  
> **Action:** get_current_time  
> **Action Input:** None  
> **Observation:** 2026-03-25 17:46:00  
>
> **Thought:** The year is 2026. I will now calculate 2026 + 10.  
> **Action:** calculator  
> **Action Input:** 2026 + 10  
> **Observation:** 2036  
>
> **Final Answer:** The current year is 2026, so 10 years from now will be 2036.