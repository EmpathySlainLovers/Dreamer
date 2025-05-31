import os
import requests
import json
from config import SYSTEM_PROMPT

# Set your API key
API_KEY = os.getenv("GROQ_API_KEY")
assert API_KEY, "Missing GROQ_API_KEY in environment variables"

# Define the base URL for Groq
url = "https://api.groq.com/openai/v1/chat/completions"

# Initialize conversation history
conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("Dreamer is awake. Say something:")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    conversation.append({"role": "user", "content": user_input})

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": conversation,
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        print("Dreamer:", reply.strip())
        conversation.append({"role": "assistant", "content": reply})
    else:
        print("Error:", response.text)
