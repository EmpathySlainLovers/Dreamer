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

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

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
