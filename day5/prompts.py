from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_chat_prompt():
    """Returns a modular chat prompt template."""
    return ChatPromptTemplate.from_messages([
        ("system", "You are a context-aware assistant. Use the chat history to maintain continuity."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])