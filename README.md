# Fullstack-Placement-Bot
# 🤖 Placement Chatbot

A **full-stack AI chatbot** for placement preparation, built with **FastAPI** (backend) and **Streamlit** (frontend).  
It can answer queries using your uploaded documents and also supports **multi-session chat history** — ideal for individual users or up to 50 users.

---

## 🌟 Features

- ChatGPT-style interface using **Streamlit**
- Multi-session chat management (up to 50 sessions)
- Document-aware responses using **FAISS vector index** and **Sentence Transformers**
- Supports multiple file formats:
  - `.pdf`, `.docx`, `.doc`, `.jpg`, `.jpeg`, `.png`
- Displays **sources** for each bot response
- Persistent chat history per session
- Floating input bar with **send button**
placement_chatbot/
├── backend/ # FastAPI backend
│ ├── app.py
│ ├── retriever.py
│ ├── indexer.py
│ ├── extractors.py
│ ├── chunker.py
│ ├── ollama_client.py
│ ├── build_docs.py
│ └── requirements.txt
├── data/ # Indexed data and raw files
│ ├── docs.jsonl
│ ├── faiss.index
│ ├── metadata.json
│ └── raw/
├── streamlit_app.py # Streamlit frontend
└── README.md


---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/placement_chatbot.git
cd placement_chatbot
2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
3. Install dependencies:
pip install -r backend/requirements.txt

📝 Setup

Add your documents to data/raw/ (PDFs, Word files, images).

Build the document JSON:
python backend/build_docs.py

Build FAISS vector index:
python backend/indexer.py

Run FastAPI backend:
uvicorn backend.app:app --reload

Run Streamlit frontend:
streamlit run streamlit_app.py

Usage:
Open the Streamlit app in your browser.
Select or create a new chat session from the sidebar.
Type your query in the input box and click Send.
View the bot responses along with document sources.
Switch between sessions anytime; chat histories are stored separately per session.

Technologies Used:
Backend: FastAPI, FAISS, Sentence Transformers, PyMuPDF, pytesseract, python-docx
Frontend: Streamlit
Models: Ollama / Gemma2 (local LLM)

Notes
Ensure you have Tesseract OCR installed for image extraction:
Tesseract OCR
Chat history is saved per session using Streamlit session_state.
Supports up to 50 concurrent user sessions.

File Upload Guide:
Place all your raw documents in data/raw/.
Supported file types: .pdf, .doc, .docx, .jpg, .jpeg, .png.
After adding files, run build_docs.py → indexer.py → start backend → start frontend.
---

## 📂 Project Structure

