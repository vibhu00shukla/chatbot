import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from chatbot_logic import get_chatbot_response, load_journal

# Load environment variables from .env file
load_dotenv()

# Set up Groq API Key
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

# Function to load journal entry
def load_journal():
    try:
        with open("journal.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No journal found."

# Streamlit page configuration
st.set_page_config(page_title="🧠 Reflecta - Your CBT Chatbot", layout="centered")
st.title("🧠 Reflecta - Your CBT Mental Health Companion")

# Load journal entry
if "journal_text" not in st.session_state:
    journal_text = load_journal()
    st.session_state.journal_text = journal_text
else:
    journal_text = st.session_state.journal_text

st.subheader("📓 Journal Reflection")
st.write(f"_{journal_text}_")

# Inject custom CSS styles
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #e5e2c1 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            color: #333 !important;
        }

        .css-1d391kg {
            color: #2C3E50;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            padding: 20px;
            margin-bottom: 20px;
        }

        .st-chat-message {
            border-radius: 20px;
            padding: 10px;
            margin: 5px 0;
        }

        .st-chat-message .user {
            background-color: #4CAF50;
            color: white;
            border-radius: 15px;
        }

        .st-chat-message .assistant {
            background-color: #F1C40F;
            color: white;
            border-radius: 15px;
        }

        .stTextInput>div>input, .stButton>button {
            border-radius: 15px !important;
            font-size: 16px;
        }

        .stButton>button {
            background-color: #2C3E50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }

        .stButton>button:hover {
            background-color: #34495E;
        }

        footer {
            text-align: center;
            color: #BDC3C7;
            font-size: 14px;
            padding-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history if not set
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You're a helpful CBT therapist AI."},
        {"role": "user", "content": f"Here's my journal entry:\n{journal_text}"}
    ]

# Display chat messages
for message in st.session_state.chat_history:
    if message["role"] == "user" and message["content"] == f"Here's my journal entry:\n{journal_text}":
        continue  # Skip displaying the journal entry again
    if message["role"] == "system":
        continue  # Skip displaying the system message again
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for chatbot
user_input = st.chat_input("Talk to Reflecta...")

if user_input:
    # Append user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Show thinking spinner
    with st.spinner("Reflecta is thinking..."):
        try:
            # Get chatbot response, passing the journal text as a part of the chat history
            reply = get_chatbot_response(st.session_state.chat_history, journal_text)
            # Append assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat messages after the conversation
for msg in st.session_state.chat_history:
    if msg["role"] == "user" and msg["content"] == f"Here's my journal entry:\n{journal_text}":
        continue  # Skip displaying the journal entry again
    if msg["role"] == "system":
        continue  # Skip displaying the system message again
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
