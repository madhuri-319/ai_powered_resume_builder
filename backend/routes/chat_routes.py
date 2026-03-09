from fastapi import APIRouter, HTTPException

from schemas.chat_schema import ChatRequest
from services.agent_runner import run_agent

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    try:
        return await run_agent(
            prompt=request.prompt,
            user_id=request.user_id,
            session_id=request.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))