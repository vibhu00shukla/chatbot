from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use your API key (hardcoded for now)
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Function to load journal
def load_journal(path="journal.txt"):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No journal found."

# Function to get chatbot response
def get_chatbot_response(chat_history, journal):
    system_prompt = f"""
You are a compassionate CBT-based mental health assistant. You have access to the following journal entry by the user:
---
{journal}
---
Use this to provide empathetic guidance, ask follow-up questions, and encourage reflection like a therapist would.
"""

    messages = [{"role": "system", "content": system_prompt}] + chat_history

    try:
        # Updated to use llama-3.3-70b-versatile model
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # New model name
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
