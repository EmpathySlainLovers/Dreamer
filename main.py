import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reinitialize Supabase with your updated project credentials
SUPABASE_URL = "https://oycvwucljzadppornhic.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95Y3Z3dWNsanphZHBwb3JuaGljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAxMTU2NDMsImV4cCI6MjA2NTY5MTY0M30.tVRBXaSgdsv3Fuwrl5B-V_-8kKKjsMZae00yVv1RLbM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Dreamer is alive and wired into OpenRouter with fresh Supabase memory!"}

# 🧠 Load past memory from Supabase
def fetch_memory():
    res = supabase.table("memory").select("*").order("id", desc=False).limit(20).execute()
    return res.data if res.data else []

# 🧠 Save new message to Supabase
def save_to_memory(role, text):
    supabase.table("memory").insert({"role": role, "text": text}).execute()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

    memory_log = fetch_memory()
    memory_log.append({"role": "user", "text": user_input})
    save_to_memory("user", user_input)

    past_messages = "\n".join([f"{m['role']}: {m['text']}" for m in memory_log])
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

        save_to_memory("assistant", reply)

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    return {"response": reply}
