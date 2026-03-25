import os
import re
from groq import Groq
from dotenv import load_dotenv
from tools import TOOL_REGISTRY
from prompts import SYSTEM_PROMPT

load_dotenv()

class ClassicAgent:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        # Each "session" should start with a fresh memory of the system prompt
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def run(self, user_query):
        self.messages.append({"role": "user", "content": user_query})
        
        for i in range(5):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            
            content = response.choices[0].message.content
            
            # --- VISIBILITY LAYER: Show the ReAct logic to the user ---
            print("\n" + "="*20 + f" STEP {i+1} " + "="*20)
            print(content) # This prints Thought, Action, and Action Input
            
            if "Final Answer:" in content:
                # We stop here because the LLM provided the final result
                break

            # Parse Action and Action Input
            action_match = re.search(r"Action:\s*(.*)", content)
            input_match = re.search(r"Action Input:\s*(.*)", content)

            if action_match and input_match:
                tool_name = action_match.group(1).strip()
                tool_input = input_match.group(1).strip()

                if tool_name in TOOL_REGISTRY:
                    observation = TOOL_REGISTRY[tool_name](tool_input)
                    
                    # --- VISIBILITY LAYER: Show the Observation ---
                    print(f"Observation: {observation}")
                    
                    self.messages.append({"role": "assistant", "content": content})
                    self.messages.append({"role": "user", "content": f"Observation: {observation}"})
                else:
                    error_msg = f"Error: Tool '{tool_name}' not found."
                    print(error_msg)
                    self.messages.append({"role": "user", "content": error_msg})
            else:
                # Fallback if the LLM format was slightly off
                break
        print("="*50 + "\n")

# MAIN EXECUTION: Completely Dynamic
if __name__ == "__main__":
    agent = ClassicAgent()
    print("--- Tool-Using AI Agent (Groq Edition) ---")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # Reset message history for a new independent query if desired, 
        # or keep it for context. Here we reset for clean testing:
        agent.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        agent.run(user_input)