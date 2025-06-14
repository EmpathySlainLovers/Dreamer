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
    return {"message": "Dreamer is alive and now using Hugging Face!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

    try:
        headers = {
            "Authorization": f"Bearer {os.environ.get('HF_API_TOKEN')}"
        }
        payload = {
            "inputs": user_input,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7
            }
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/TheBloke/Nous-Hermes-2-Mistral-7B-DPO-GGUF",
            headers=headers,
            json=payload
        )
        hf_result = response.json()
        reply = hf_result[0]['generated_text'].split(user_input)[-1].strip()
    except Exception as e:
        reply = f"Error: {e}"

    return {"response": reply}
