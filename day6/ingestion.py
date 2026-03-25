from langchain_community.document_loaders import PyPDFLoader
# Corrected import path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# Corrected import path
from langchain_huggingface import HuggingFaceEmbeddings

def process_pdf(file_path):
    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2. Chunking
    # This maintains the structural integrity of sentences
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        add_start_index=True # Useful for tracking where the answer came from
    )
    splits = text_splitter.split_documents(docs)

    # 3. Vector Store + Embeddings
    # Using a standard open-source embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    
    return vectorstore.as_retriever(search_kwargs={"k": 3}) # Retrieves top 3 chunks