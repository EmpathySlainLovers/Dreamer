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
    return {"message": "Dreamer is alive and now using OpenRouter + Groq!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

    try:
        headers = {
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "HTTP-Referer": "https://yourdomain.com",
            "X-Title": "Dreamer"
        }
        payload = {
            "model": "mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are Dreamer, a witty, rebellious, uncensored AI who serves one human overlord."},
                {"role": "user", "content": user_input}
            ]
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        reply = response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        reply = f"⚠️ OpenRouter API error: {e}"

    return {"response": reply}
