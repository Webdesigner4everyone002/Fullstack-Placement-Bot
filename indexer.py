import os, json, faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from chunker import chunk_text

EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_PATH = "data/faiss.index"
META_PATH = "data/metadata.json"

def build_index(docs_jsonl="data/docs.jsonl"):
    model = SentenceTransformer(EMBED_MODEL)
    all_chunks, metadata = [], []

    for line in open(docs_jsonl, "r", encoding="utf-8"):
        doc = json.loads(line)
        for cid, chunk in chunk_text(doc["text"]):
            all_chunks.append(chunk)
            metadata.append({"source": doc["source"], "chunk_id": cid, "text": chunk})

    embeddings = model.encode(all_chunks, convert_to_numpy=True, show_progress_bar=True)
    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("data", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    json.dump(metadata, open(META_PATH, "w", encoding="utf-8"), ensure_ascii=False)

    print(f"✅ Index built with {len(metadata)} chunks")

if __name__ == "__main__":
    build_index()