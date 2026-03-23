import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def start_chatbot():
    # Initialize Groq client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env file.")
        return

    client = Groq(api_key=api_key)
    
    print("--- Free LLM Chatbot (Groq/Llama 3) ---")
    print("Type 'exit' to quit.\n")
    
    while True:
        # Input: User prompt from terminal
        user_input = input("User: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input:
            continue

        try:
            # API Call
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_input}],
            )

            # Output: LLM-generated response
            answer = completion.choices[0].message.content
            print(f"\nAssistant: {answer}")

            # Constraints: Print token usage
            usage = completion.usage
            print(f"\n[Usage: Prompt={usage.prompt_tokens}, "
                  f"Completion={usage.completion_tokens}, Total={usage.total_tokens}]\n")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_chatbot()