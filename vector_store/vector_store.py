import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/meta.pkl"

# Use the same model as build_index.py
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

def embed(text: str):
    return model.encode(text, convert_to_numpy=True).astype('float32')

def search(query: str, top_k: int = 5):
    """Search for similar documents"""
    query_vec = embed(query)
    query_vec = np.array([query_vec])
    
    distances, indices = index.search(query_vec, top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            results.append({
                "text": metadata[idx],
                "score": float(distances[0][i])
            })
    
    return results