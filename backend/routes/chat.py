"""Chat analytics routes — conversational Q&A on financial data."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents.chat_analytics import ChatAnalyticsAgent
from services.store import store

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    upload_id: str
    message: str
    session_id: Optional[str] = "default"


@router.post("/send")
async def send_message(msg: ChatMessage):
    """Send a message and get AI analysis response."""
    # Get chat history for this session
    history = store.find("chat_history", {"session_id": msg.session_id, "upload_id": msg.upload_id})

    # Save user message
    store.append("chat_history", {
        "session_id": msg.session_id,
        "upload_id": msg.upload_id,
        "role": "user",
        "content": msg.message
    })

    # Get AI response
    agent = ChatAnalyticsAgent()
    try:
        result = await agent.chat(msg.upload_id, msg.message, history)
    except Exception as e:
        raise HTTPException(500, f"Chat error: {str(e)}")

    # Save assistant response
    answer = result.get("answer", str(result))
    store.append("chat_history", {
        "session_id": msg.session_id,
        "upload_id": msg.upload_id,
        "role": "assistant",
        "content": answer
    })

    return {"status": "success", "data": result}


@router.get("/history/{session_id}")
async def get_history(session_id: str, upload_id: str = None):
    """Get chat history for a session."""
    filters = {"session_id": session_id}
    if upload_id:
        filters["upload_id"] = upload_id
    history = store.find("chat_history", filters)
    return {"status": "success", "data": history}


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """Clear chat history for a session."""
    deleted = store.delete("chat_history", {"session_id": session_id})
    return {"status": "success", "deleted": deleted}
