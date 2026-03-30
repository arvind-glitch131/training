# Multi-Step Workflow Agent (LangGraph)

An advanced stateful AI orchestrator built with LangGraph and Groq. Unlike standard linear agents, this workflow uses a State Machine to plan, execute, and iterate through complex problems step-by-step.

---

## 🚀 Features

* **Explicit State Management**: Uses a TypedDict to maintain a "shared memory" across different execution nodes.  
* **Planning & Execution Pattern**: Separates the "Thinking" (Planning) from the "Doing" (Solving) for higher accuracy.  
* **Conditional Branching**: Implements a supervisor logic that checks if more steps are required before finishing.  
* **Cyclic Workflows**: Supports looping back to specific nodes until a termination condition is met.  

---

## 🏗️ Architecture & Concepts

The project is built on four pillars:

* **State (AgentState)**: A persistent object carrying the problem, the plan, the current progress, and the evolving solution.  
* **Nodes**: Independent functions (`planner`, `solver`) that perform specific transformations on the State.  
* **Edges**: Defined paths that control the movement between nodes.  
* **Conditional Edges**: Logic gates that decide whether to continue solving or transition to the end.  

---

## 🛠️ Tech Stack

* **Framework**: langgraph (v1.1+ / v0.3+ compatible)  
* **Orchestration**: langchain-core  
* **LLM**: llama-3.3-70b-versatile (via Groq)  
* **Environment**: Python 3.14+  

---

## 📂 Project Structure

    day10_langgraph/
    ├── state.py      # Definition of the TypedDict State
    ├── nodes.py      # Python functions for Planning and Solving
    ├── graph.py      # Construction of the StateGraph and Edges
    ├── main.py       # Orchestrator to stream and run the graph
    ├── .env          # Groq API Key
    └── requirements.txt

---

## 🔄 Workflow Logic

1. **START**: The user provides a problem (e.g., "How to build a chair?").  
2. **Planner Node**: The LLM breaks the problem into a list of 3 logical steps.  
3. **Solver Node**: The LLM takes the current step from the list and writes a detailed solution.  
4. **Decision Gate**: A conditional edge checks: Is `current_step < total_steps`?  

   - If **True**: Loops back to the Solver Node.  
   - If **False**: Moves to END.  

5. **FINISH**: The final accumulated solution is printed from the state.  

---

## ⚙️ Setup & Execution

### 1. Install Dependencies

    pip install -r requirements.txt

### 2. Set Environment Variables

Create a `.env` file with:

    GROQ_API_KEY=your_key_here

### 3. Run the Workflow

    python main.py

---