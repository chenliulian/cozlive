"""
记忆路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def store_memory():
    return {"memory_id": "mem-001"}

@router.get("/retrieve")
async def retrieve_memory():
    return {"memories": []}

@router.get("/agent/{agent_id}")
async def get_agent_memories(agent_id: str):
    return {"agent_id": agent_id, "memories": []}
