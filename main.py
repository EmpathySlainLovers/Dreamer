import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Dreamer is alive and wired into OpenRouter!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

    # Load Dreamer's personality from file
    try:
        with open("personality.txt", "r") as f:
            personality = f.read()
    except Exception as e:
        personality = "You are Dreamer, an AI assistant. Respond helpfully and with attitude."

    # Load memory
    try:
        with open("memory.json", "r") as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        memory_data = {"log": []}

    # Add user message to memory
    memory_data["log"].append({"role": "user", "content": user_input})

    # Prepare message history for OpenRouter format
    messages = [{"role": "system", "content": personality}]
    for entry in memory_data["log"]:
        messages.append({"role": entry["role"], "content": entry["content"]})

    # API call to OpenRouter
    try:
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "HTTP-Referer": "https://dreamer.com",
            "X-Title": "Dreamer"
        }
        payload = {
            "model": "sentientagi/dobby-mini-unhinged-plus-llama-3.1-8b",
            "messages": messages,
            "temperature": 0.8
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        hf_result = response.json()
        reply = hf_result["choices"][0]["message"]["content"]

        # Save reply to memory
        memory_data["log"].append({"role": "assistant", "content": reply})
        with open("memory.json", "w") as f:
            json.dump(memory_data, f)

    except Exception as e:
        reply = f"⚠️ OpenRouter API error: {e}"

    return {"response": reply}
