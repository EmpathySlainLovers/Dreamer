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
    return {"message": "Dreamer is alive and deployed!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")
    return {"response": f"Echo: {user_input}"}
