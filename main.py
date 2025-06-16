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
                "max_new_tokens": 150,
                "temperature": 0.75
            }
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/TheBloke/Nous-Hermes-2-Mistral-7B-DPO-GGUF",
            headers=headers,
            json=payload
        )
        hf_result = response.json()

        # Handle both common response formats
        if isinstance(hf_result, dict) and "generated_text" in hf_result:
            reply = hf_result["generated_text"]
        elif isinstance(hf_result, list) and "generated_text" in hf_result[0]:
            reply = hf_result[0]["generated_text"]
        else:
            reply = "⚠️ No valid response from Hugging Face."

    except Exception as e:
        reply = f"💥 Error: {str(e)}"

    return {"response": reply}
