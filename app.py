from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from retriever import load_index, retrieve
from ollama_client import call_ollama
from collections import deque

# ==========================
# App Initialization
# ==========================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://127.0.0.1:5500"] if using VSCode Live Server
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Models
# ==========================
class Query(BaseModel):
    user_id: str  # Unique ID for each user
    question: str

# ==========================
# Load Index
# ==========================
index, metadata, model = load_index()

# ==========================
# Conversation Management
# ==========================
MAX_USERS = 50
MAX_HISTORY = 20
conversation_store = {}  # user_id -> deque of messages

# ==========================
# Health Check Endpoint
# ==========================
@app.get("/health")
def health():
    return {"status": "ok"}

# ==========================
# Query Endpoint
# ==========================
@app.post("/query")
def query_api(q: Query):
    # Get user history
    user_history = conversation_store.get(q.user_id, deque(maxlen=MAX_HISTORY))

    # Retrieve relevant context from documents
    contexts = retrieve(q.question, index, metadata, model, top_k=3)
    filtered_contexts = [c for c in contexts if c.get("text") and c["text"].strip()]
    ctx_text = "\n\n".join([c["text"] for c in filtered_contexts])

    # Build conversation history text
    history_text = ""
    for msg in user_history:
        role = "USER" if msg["role"] == "user" else "ASSISTANT"
        history_text += f"{role}: {msg['text']}\n"

    # Construct the prompt for the model
    if not ctx_text:
        prompt = f"""
You are a helpful AI assistant. Answer the question concisely.
Conversation so far:
{history_text}
USER: {q.question}
"""
    else:
        prompt = f"""
You are a helpful AI assistant. Use the following CONTEXT to answer the question.
CONTEXT:
{ctx_text}

Conversation so far:
{history_text}
USER: {q.question}
"""

    # Call the Ollama model
    answer = call_ollama(prompt, model="llama3.2:1b")

    # Update conversation history
    if q.user_id not in conversation_store:
        # Trim oldest user if exceeding MAX_USERS
        if len(conversation_store) >= MAX_USERS:
            conversation_store.pop(next(iter(conversation_store)))
        conversation_store[q.user_id] = deque(maxlen=MAX_HISTORY)

    conversation_store[q.user_id].append({"role": "user", "text": q.question})
    conversation_store[q.user_id].append({"role": "assistant", "text": answer})

    return {"answer": answer, "sources": [c["source"] for c in contexts]}

# ==========================
# Optional: Get Chat History
# ==========================
@app.get("/history/{user_id}")
def get_history(user_id: str):
    history = conversation_store.get(user_id, [])
    return {"history": list(history)}
