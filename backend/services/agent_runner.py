
import uuid
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.query_agent import root_agent

APP_NAME = "SkillFlow_AI"

session_service = InMemorySessionService()

runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service
)


async def run_agent(prompt: str, user_id: str = "default_user", session_id: str | None = None):

    session_id = session_id or str(uuid.uuid4())

    await session_service.create_session(
        user_id=user_id,
        session_id=session_id,
        app_name=APP_NAME
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt)]
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

        elif hasattr(event, "content") and event.content:
            if hasattr(event.content, "parts"):
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        reply += part.text

    return {
        "session_id": session_id,
        "reply": reply
    }
