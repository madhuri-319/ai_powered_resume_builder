import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# 1. Load your API Key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# 2. Enable CORS so Angular can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "models/gemini-2.5-flash" # Optimized for 2026 speed

class ChatRequest(BaseModel):
    prompt: str

# Optional: Store history in memory (Reset when server restarts)
chat_history = []

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    global chat_history
    try:
        # Add user message to history
        chat_history.append({"role": "user", "parts": [{"text": request.prompt}]})

        # Generate content using your working Colab logic
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=chat_history
        )

        reply = response.text
        
        # Add AI response to history to maintain context
        chat_history.append({"role": "model", "parts": [{"text": reply}]})

        return {"reply": reply}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))