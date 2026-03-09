from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    user_id: str = "default_user"
    session_id: str | None = None