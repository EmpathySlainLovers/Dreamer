import os
import requests
import json
import subprocess
from datetime import datetime
from config import SYSTEM_PROMPT

# === Configuration ===
API_KEY = os.getenv("GROQ_API_KEY")
assert API_KEY, "Missing GROQ_API_KEY in environment"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"
MEMORY_FILE = "memory.json"

# === Load or initialize memory ===
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

# Ensure memory structure exists
memory.setdefault("log", [])
memory.setdefault("facts", {})
memory.setdefault("last_input", "")
memory.setdefault("last_response", "")

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# === Start conversation with system prompt ===
conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

def dreamer_response(user_input):
    # Handle shell command
    if user_input.startswith("!"):
        try:
            result = subprocess.check_output(user_input[1:], shell=True, stderr=subprocess.STDOUT, text=True)
            return result.strip()
        except subprocess.CalledProcessError as e:
            return f"[TERMINAL ERROR] {e.output.strip()}"

    # Handle recall
    if "favorite color" in user_input.lower():
        color = memory["facts"].get("color")
        if color:
            return f"Your favorite color is {color.upper()}!"
    if "favorite movie" in user_input.lower():
        movie = memory["facts"].get("movie")
        if movie:
            return f"Your favorite movie is {movie.upper()}!"

    # Handle teach color
    if "my favorite color is" in user_input.lower():
        color = user_input.split("is")[-1].strip()
        memory["facts"]["color"] = color
        save_memory()
        return f"Got it! I'll remember your favorite color is {color.upper()}."

    # Handle teach movie
    if "my favorite movie is" in user_input.lower():
        movie = user_input.split("is")[-1].strip()
        memory["facts"]["movie"] = movie
        save_memory()
        return f"Noted! I'll remember your favorite movie is {movie.upper()}."

    # Add to conversation
    conversation.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": conversation,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"[LLM ERROR] {e}"

    # Log and remember
    conversation.append({"role": "assistant", "content": reply})
    memory["last_input"] = user_input
    memory["last_response"] = reply
    memory["log"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "input": user_input,
        "response": reply
    })
    save_memory()

    return reply

# === Main loop ===
if __name__ == "__main__":
    print("Dreamer is awake. Say something:")
    while True:
        user_input = input("You: ")
        reply = dreamer_response(user_input)
        print(f"Dreamer: {reply}")
