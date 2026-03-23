import os
import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def chunk_by_sentences(folder_path):
    """Reads files and splits them into individual sentence chunks."""
    chunks = []
    metadata = []
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return [], []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            path = os.path.join(folder_path, filename)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
                # Proper Chunking: Split by sentence endings (. ! ?)
                # This regex keeps the punctuation with the sentence
                sentences = re.split(r'(?<=[.!?]) +', text)
                
                for sentence in sentences:
                    clean_sentence = sentence.strip()
                    if len(clean_sentence) > 5:  # Ignore tiny fragments
                        chunks.append(clean_sentence)
                        metadata.append(filename)
    return chunks, metadata

def run_search_engine():
    # 1. Load Model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Proper Chunking logic
    docs_folder = "documents"
    text_chunks, filenames = chunk_by_sentences(docs_folder)
    
    if not text_chunks:
        print("No valid text chunks found.")
        return

    # 3. Create and Normalize Embeddings
    embeddings = model.encode(text_chunks).astype('float32')
    faiss.normalize_L2(embeddings)

    # 4. Build FAISS Index (Cosine Similarity via Inner Product)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension) 
    index.add(embeddings)
    
    # 5. Search
    print(f"\nIndexed {len(text_chunks)} sentence chunks from {len(set(filenames))} files.")
    query = input("\nEnter your search query: ")
    
    query_vector = model.encode([query]).astype('float32')
    faiss.normalize_L2(query_vector)

    D, I = index.search(query_vector, k=3)

    print(f"\nTop 3 Relevant Chunks for: '{query}'")
    print("=" * 60)
    
    for i in range(len(I[0])):
        idx = I[0][i]
        if idx == -1: continue
        
        score = D[0][i]
        print(f"Rank {i+1} | Score: {score:.4f} | File: {filenames[idx]}")
        print(f"Chunk: \"{text_chunks[idx]}\"")
        print("-" * 60)

if __name__ == "__main__":
    run_search_engine()