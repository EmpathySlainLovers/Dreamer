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
    return {"message": "Dreamer is alive and connected to Hugging Face!"}

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
    "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",

            headers=headers,
            json=payload
        )
        hf_result = response.json()

        # Try to extract reply safely
        if isinstance(hf_result, list) and "generated_text" in hf_result[0]:
            reply = hf_result[0]["generated_text"].split(user_input)[-1].strip()
        elif "error" in hf_result:
            reply = f"⚠️ HF API error: {hf_result['error']}"
        else:
            reply = "⚠️ No valid response from Hugging Face."
    except Exception as e:
        reply = f"⚠️ Server error: {e}"

    return {"response": reply}
