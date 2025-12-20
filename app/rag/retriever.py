import faiss
import pickle
from sentence_transformers import SentenceTransformer

VECTOR_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/meta.pkl"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index(VECTOR_PATH)

with open(META_PATH, "rb") as f:
    documents = pickle.load(f)

def retrieve(query: str, top_k: int = 5):
    q_emb = model.encode([query])
    _, indices = index.search(q_emb, top_k)
    return [documents[i] for i in indices[0]]
