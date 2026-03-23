import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

def get_groq_client():
    """Initializes the Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)

def read_questions(file_path):
    """Reads questions from a .txt file."""
    try:
        with open(file_path, 'r') as f:
            # Filters out empty lines
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

def ask_groq(client, question):
    """Sends a question to Groq with a constraint for brevity."""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                # System message sets the behavior of the LLM
                {"role": "system", "content": "You are a concise assistant. Provide answers in 3 lines or less."},
                {"role": "user", "content": question}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def save_results(data, output_path):
    """Saves results to a JSON file."""
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"File saved successfully to {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    client = get_groq_client()
    questions = read_questions("questions.txt")
    
    if not questions:
        print("No questions to process.")
        return

    final_results = []
    for q in questions:
        print(f"Asking: {q}")
        ans = ask_groq(client, q)
        final_results.append({
            "question": q,
            "answer": ans
        })

    save_results(final_results, "answers.json")

if __name__ == "__main__":
    main()