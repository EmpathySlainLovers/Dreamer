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

# Load Dreamer's personality from personality.txt
try:
    with open("personality.txt", "r") as f:
        system_prompt = f.read()
except FileNotFoundError:
    system_prompt = "You are Dreamer. Personality file not found. Defaulting to basic behavior."

@app.get("/")
def root():
    return {"message": "Dreamer is alive and wired into OpenRouter!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

    # Load memory log
    try:
        with open("memory.json", "r") as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        memory_data = {"log": []}

    # Add current input to memory
    memory_data["log"].append({"role": "user", "text": user_input})

    try:
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "HTTP-Referer": "https://dreamer.com",
            "X-Title": "Dreamer"
        }
        payload = {
            "model": "sentientagi/dobby-mini-unhinged-plus-llama-3.1-8b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.8
        }

                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
            memory_data["log"].append({"role": "assistant", "text": reply})
            with open("memory.json", "w") as f:
                json.dump(memory_data, f)
        else:
            reply = f"⚠️ OpenRouter API error: {result}"


        # Add Dreamer's reply to memory
        memory_data["log"].append({"role": "assistant", "text": reply})

        # Save memory
        with open("memory.json", "w") as f:
            json.dump(memory_data, f)

    except Exception as e:
        reply = f"⚠️ OpenRouter API error: {e}"

    return {"response": reply}
