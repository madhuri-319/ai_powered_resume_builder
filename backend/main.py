import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.query_agent import root_agent

load_dotenv()

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ADK Runner Setup
# -----------------------------
session_service = InMemorySessionService()

runner = Runner(
    app_name="SkillFlow_AI",
    agent=root_agent,
    session_service=session_service
)

APP_NAME = "SkillFlow_AI"

# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    prompt: str
    user_id: str = "default_user"
    session_id: str | None = None


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/api/chat")
async def chat(request: ChatRequest):

    try:

        user_id = request.user_id

        # generate session if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # ALWAYS create session (safe for InMemorySessionService)
        await session_service.create_session(
            user_id=user_id,
            session_id=session_id,
            app_name=APP_NAME
        )

        # convert user message
        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=request.prompt)]
        )

        events = runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        )

        reply = ""

        for event in events:

            if hasattr(event, "text") and event.text:
                reply += event.text

            elif hasattr(event, "content"):
                if hasattr(event.content, "parts"):
                    for part in event.content.parts:
                        if hasattr(part, "text"):
                            reply += part.text

        return {
            "session_id": session_id,
            "reply": reply
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))