import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from ingestion import process_documents_from_folder
from prompts import get_source_rag_prompt

# Load environment variables
load_dotenv()

def main():
    # 1. Configuration
    folder_path = "data" 
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Directory '{folder_path}' created. Add your documents and restart.")
        return

    # 2. Initialize LLM (Groq Free Tier)
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # 3. Ingestion
    print(f"Indexing all documents in '{folder_path}'...")
    vectorstore = process_documents_from_folder(folder_path)
    
    if vectorstore is None:
        return

    # Use the updated prompt that demands inline citations
    prompt_template = get_source_rag_prompt()

    print("\n--- RAG System: Explicit Citations Enabled ---")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nQuestion: ")
        if query.lower() in ["exit", "quit"]:
            break

        # 4. Retrieval (Top-K Similarity Search)
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs:
            print("AI: I found no relevant information in your documents.")
            continue

        # 5. Context Construction with Source Prefixing
        # This "tags" every chunk so the LLM knows its origin
        context_parts = []
        unique_sources = []

        for doc in docs:
            # Clean the file path to just the name
            file_name = os.path.basename(doc.metadata.get('source', 'Unknown File'))
            page_num = doc.metadata.get('page', 'N/A')

            # Create a header for this specific chunk
            header = f"[SOURCE: {file_name}]"
            context_parts.append(f"{header}\n{doc.page_content}")

            # Collect for the footer references
            ref_str = f"{file_name}"
            if isinstance(page_num, int):
                ref_str += f" (Page {page_num + 1})"
            
            if ref_str not in unique_sources:
                unique_sources.append(ref_str)

        # Join chunks with clear separators
        full_context = "\n\n---\n\n".join(context_parts)

        # 6. Execution
        formatted_prompt = prompt_template.format(
            context=full_context, 
            question=query
        )
        
        try:
            response = llm.invoke(formatted_prompt)
            
            # 7. Output Result + Footer References
            print(f"\nAnswer: {response.content}")
            print("\nRetrieved from:")
            for s in unique_sources:
                print(f"📍 {s}")
                
        except Exception as e:
            print(f"Error during generation: {e}")

if __name__ == "__main__":
    main()