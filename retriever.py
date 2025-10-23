import faiss, json
from sentence_transformers import SentenceTransformer
import numpy as np

EMBED_MODEL = "all-MiniLM-L6-v2"

def load_index(index_path="data/faiss.index", meta_path="data/metadata.json"):
    index = faiss.read_index(index_path)
    metadata = json.load(open(meta_path, encoding="utf-8"))
    model = SentenceTransformer(EMBED_MODEL)
    return index, metadata, model

def retrieve(query, index, metadata, model, top_k=5):
    q_emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, top_k)
    results = []
    for score, idx in zip(D[0], I[0]):
        if idx < 0: continue
        entry = metadata[idx]
        results.append({"score": float(score), **entry})
    return results