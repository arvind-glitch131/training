from langchain_core.prompts import ChatPromptTemplate

def get_rag_prompt():
    template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}
    """
    return ChatPromptTemplate.from_template(template)