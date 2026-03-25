import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def process_documents_from_folder(folder_path):
    """
    Loads all PDFs and Text files from a folder, chunks them, 
    and creates a FAISS vector store.
    """
    all_docs = []

    # 1. Iterate through the folder
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return None

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Handle PDFs
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            all_docs.extend(loader.load())
        
        # Handle Text Files
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
            all_docs.extend(loader.load())

    if not all_docs:
        print("No valid documents found in the folder.")
        return None

    # 2. Chunking (Preserves metadata like 'source' and 'page' automatically)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(all_docs)

    # 3. Vector Store + Local Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    
    return vectorstore