import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

    # Load system personality from personality.txt
    try:
        with open("personality.txt", "r") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        system_prompt = "You're Dreamer. Respond in a confident and helpful tone."

    # Load memory
    try:
        with open("memory.json", "r") as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        memory_data = {"log": []}

    # Add user message
    memory_data["log"].append({"role": "user", "text": user_input})

    # Build messages array
    messages = [{"role": "system", "content": system_prompt}]
    for m in memory_data["log"]:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["text"]})

    # Send to OpenRouter
    try:
        headers = {
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "HTTP-Referer": "https://dreamer.com",
            "X-Title": "Dreamer"
        }
        payload = {
            "model": "sentientagi/dobby-mini-unhinged-plus-llama-3.1-8b",
            "messages": messages,
            "temperature": 0.85
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
