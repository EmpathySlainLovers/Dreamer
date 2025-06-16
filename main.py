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

    # Load personality.txt
    try:
        with open("personality.txt", "r") as f:
            personality_prompt = f.read().strip()
    except FileNotFoundError:
        personality_prompt = "You are Dreamer, an AI assistant."

    # Load memory
    try:
        with open("memory.json", "r") as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        memory_data = {"log": []}

    # Add current input to memory
    memory_data["log"].append({"role": "user", "text": user_input})

    # Prepare messages payload
    messages = [{"role": "system", "content": personality_prompt}]
    for m in memory_data["log"]:
        messages.append({"role": m["role"], "content": m["text"]})

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

        if "choices" in hf_result and len(hf_result["choices"]) > 0:
            reply = hf_result["choices"][0]["message"]["content"]
        else:
            reply = "⚠️ No valid response from OpenRouter."

        # Save Dreamer's reply to memory
        memory_data["log"].append({"role": "assistant", "text": reply})
        with open("memory.json", "w") as f:
            json.dump(memory_data, f)

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    return {"response": reply}
