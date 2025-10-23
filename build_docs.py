import os, json
from extractors import extract_text_from_file

RAW_DIR = "data/raw"
OUT_JSONL = "data/docs.jsonl"

def build_docs():
    os.makedirs("data", exist_ok=True)
    with open(OUT_JSONL, "w", encoding="utf-8") as out:
        for fname in os.listdir(RAW_DIR):
            path = os.path.join(RAW_DIR, fname)
            if os.path.isfile(path):
                text = extract_text_from_file(path)
                doc = {"source": fname, "text": text}
                out.write(json.dumps(doc, ensure_ascii=False) + "\n")
    print("✅ Docs saved to", OUT_JSONL)

if __name__ == "__main__":
    build_docs()