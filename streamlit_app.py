import streamlit as st
import requests
from datetime import datetime

# --------------------------
# Page Setup
# --------------------------
st.set_page_config(
    page_title="Placement Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------
# Session Management
# --------------------------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}  # key: session_id, value: chat history

if "current_session" not in st.session_state:
    st.session_state.current_session = f"Session_{datetime.now().strftime('%H%M%S')}"

# Sidebar: switch/create sessions
st.sidebar.title("💬 Chat Sessions")

for session_id in list(st.session_state.sessions.keys()):
    if st.sidebar.button(session_id):
        st.session_state.current_session = session_id

if st.sidebar.button("➕ New Session"):
    new_session = f"Session_{datetime.now().strftime('%H%M%S')}"
    st.session_state.current_session = new_session
    st.session_state.sessions[new_session] = []

st.sidebar.markdown("---")
st.sidebar.write(f"**Current Session:** {st.session_state.current_session}")

# Initialize chat history
if st.session_state.current_session not in st.session_state.sessions:
    st.session_state.sessions[st.session_state.current_session] = []

chat_history = st.session_state.sessions[st.session_state.current_session]

# --------------------------
# Function to call backend API
# --------------------------
def get_bot_response(message):
    payload = {
        "question": message,
        "user_id": st.session_state.current_session  # send the session ID as user_id
    }
    try:
        resp = requests.post("http://127.0.0.1:8000/query", json=payload)
        if resp.ok:
            data = resp.json()
            return data.get("answer", "No answer returned."), data.get("sources", [])
        else:
            return f"Error: {resp.text}", []
    except Exception as e:
        return f"Error: {str(e)}", []


# --------------------------
# Chat Display Container
# --------------------------
chat_container = st.container()

def render_chat():
    with chat_container:
        for chat in chat_history:
            if chat["role"] == "user":
                st.markdown(
                    f"""
                    <div style='text-align: right; background-color: #DCF8C6; padding:10px; 
                    border-radius:15px; margin:5px 0; max-width:70%; float:right; clear:both;'>
                    {chat['message']}
                    </div>
                    """, unsafe_allow_html=True
                )
            else:
                sources_text = ""
                if chat.get("sources"):
                    sources_text = "<br><i>Sources: " + ", ".join(chat["sources"]) + "</i>"
                st.markdown(
                    f"""
                    <div style='text-align: left; background-color: #F1F0F0; padding:10px; 
                    border-radius:15px; margin:5px 0; max-width:70%; float:left; clear:both;'>
                    {chat['message']}
                    {sources_text}
                    </div>
                    """, unsafe_allow_html=True
                )

render_chat()

# --------------------------
# Floating Input Box
# --------------------------
st.markdown(
    """
    <style>
        .input-box {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #FFF;
            padding: 10px;
            border-top: 1px solid #CCC;
            display: flex;
            align-items: center;
        }
        .input-box input[type="text"] {
            width: 80%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #CCC;
        }
        .input-box button {
            width: 15%;
            margin-left: 5px;
            padding: 10px;
            border-radius: 5px;
            border: none;
            background-color: #10A37F;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
    """, unsafe_allow_html=True
)

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="chat_input")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    # Add user message
    chat_history.append({"role": "user", "message": user_input})
    
    # Get bot response
    answer, sources = get_bot_response(user_input)
    chat_history.append({"role": "bot", "message": answer, "sources": sources})
    
    # Save updated history
    st.session_state.sessions[st.session_state.current_session] = chat_history
    
    # Rerender chat without rerun
    render_chat()
