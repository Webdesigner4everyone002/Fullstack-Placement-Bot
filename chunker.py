def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    i = 0
    cid = 0
    while i < len(text):
        end = min(i + chunk_size, len(text))
        chunk = text[i:end].strip()
        if len(chunk) > 50:  # skip tiny chunks
            chunks.append((cid, chunk))
            cid += 1
        i += chunk_size - overlap
    return chunks