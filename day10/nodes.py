from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from state import AgentState  # Add this line
# ... rest of your code

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def problem_planner(state: AgentState):
    """Breaks the problem into a 3-step plan."""
    print("--- PLANNING ---")
    prompt = f"Break this problem into exactly 3 logical steps: {state['problem']}"
    response = llm.invoke(prompt)
    # Split by lines or just save the content
    steps = [s.strip() for s in response.content.split('\n') if s.strip()][:3]
    return {"steps": steps, "current_step": 0}

def step_solver(state: AgentState):
    """Solves the current step in the list."""
    current_idx = state['current_step']
    step_to_solve = state['steps'][current_idx]
    print(f"--- SOLVING STEP {current_idx + 1}: {step_to_solve} ---")
    
    response = llm.invoke(f"Solve this specific step: {step_to_solve}")
    
    # Append the solution to the existing solution string
    new_solution = state.get('solution', "") + f"\nStep {current_idx+1}: {response.content}\n"
    
    return {"solution": new_solution, "current_step": current_idx + 1}