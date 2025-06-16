import os
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

import json

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

    # Load memory
    try:
        with open("memory.json", "r") as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        memory_data = {"log": []}

    # Add current input to memory
    memory_data["log"].append({"role": "user", "text": user_input})

    # Prepare full memory context
    past_messages = "\n".join([f"{m['role']}: {m['text']}" for m in memory_data["log"]])
    full_prompt = f"{past_messages}\nDreamer:"

    try:
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "HTTP-Referer": "https://dreamer.com",
            "X-Title": "Dreamer"
        }
        payload = {
            "model": "sentientagi/dobby-mini-unhinged-plus-llama-3.1-8b",
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": 0.8
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        hf_result = response.json()
        reply = hf_result["choices"][0]["message"]["content"]

        # Add Dreamer's reply to memory
        memory_data["log"].append({"role": "assistant", "text": reply})

        # Save memory
        with open("memory.json", "w") as f:
            json.dump(memory_data, f)

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    return {"response": reply}


    try:
        headers = {
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "sentientagi/dobby-mini-unhinged-plus-llama-3.1-8b",
            "messages": [{"role": "user", "content": user_input}]
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        hf_result = response.json()
        reply = hf_result['choices'][0]['message']['content']
    except Exception as e:
        import traceback
        traceback.print_exc()
        reply = f"⚠️ OpenRouter API error: {e}"

    return {"response": reply}
