"""
聊天路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/message")
async def send_message():
    return {"message": "Message sent"}

@router.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    return {"conversation_id": conversation_id, "messages": []}

@router.post("/conversations")
async def create_conversation():
    return {"conversation_id": "new-conv"}
