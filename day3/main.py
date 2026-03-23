from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

def load_sentences(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    input_file = "data.txt"
    output_file = "results.txt"
    
    sentences = load_sentences(input_file)
    if len(sentences) < 2:
        print("Need at least two sentences.")
        return

    # Initialize model and generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    sim_matrix = cosine_similarity(embeddings)

    # Process pairs
    pairs = []
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            pairs.append({
                "pair": (sentences[i], sentences[j]),
                "score": sim_matrix[i][j]
            })
    
    pairs.sort(key=lambda x: x['score'], reverse=True)

    # Write results to txt file
    with open(output_file, 'w') as f:
        f.write(f"Semantic Similarity Analysis\n")
        f.write(f"Source: {input_file}\n")
        f.write("-" * 30 + "\n\n")
        
        f.write("--- All Similarity Scores ---\n")
        for res in pairs:
            f.write(f"[{res['score']:.4f}] {res['pair'][0]} | {res['pair'][1]}\n")
        
        if pairs:
            f.write("\n--- Top Most Similar Pair ---\n")
            top = pairs[0]
            f.write(f"Sentence 1: {top['pair'][0]}\n")
            f.write(f"Sentence 2: {top['pair'][1]}\n")
            f.write(f"Similarity Score: {top['score']:.4f}\n")

    print(f"Analysis complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()