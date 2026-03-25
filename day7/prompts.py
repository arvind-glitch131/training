from langchain_core.prompts import ChatPromptTemplate

def get_source_rag_prompt():
    template = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    
    CRITICAL INSTRUCTION: For every claim you make, you MUST cite the source name 
    at the end of the sentence (e.g., "Sourdough requires a starter [document.pdf]"). 
    If the context doesn't contain the answer, say you don't know.

    Context: {context}
    
    Question: {question}
    
    Answer:"""
    return ChatPromptTemplate.from_template(template)