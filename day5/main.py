import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from prompts import get_chat_prompt

load_dotenv()

# Dictionary to store session histories in memory
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def main():
    # 1. Initialize Groq (Free Tier Model)
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5
    )

    # 2. Build the LCEL Chain
    prompt = get_chat_prompt()
    chain = prompt | llm

    # 3. Wrap with Message History (The Modern "Memory" approach)
    with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    # 4. Interaction Loop
    print("Groq-Powered Chatbot (2026 LCEL Standard). Type 'exit' to stop.")
    config = {"configurable": {"session_id": "user_1"}}

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = with_message_history.invoke(
            {"input": user_input},
            config=config
        )
        print(f"AI: {response.content}\n")

if __name__ == "__main__":
    main()