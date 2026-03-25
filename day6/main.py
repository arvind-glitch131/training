import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from ingestion import process_pdf
from prompts import get_rag_prompt

load_dotenv()

def main():
    # Initialize LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    # Initialize Retriever (Update path to your PDF)
    pdf_path = "document.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        return

    retriever = process_pdf(pdf_path)
    prompt = get_rag_prompt()

    # LCEL Chain: Context Retrieval -> Prompt Formatting -> LLM -> String Output
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Execution
    print("RAG System Ready. Ask a question about your PDF (type 'exit' to quit):")
    while True:
        query = input("Question: ")
        if query.lower() == "exit":
            break
        
        response = rag_chain.invoke(query)
        print(f"\nAnswer: {response}\n")

if __name__ == "__main__":
    main()