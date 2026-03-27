"""
Agent 路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_agent():
    return {"message": "Agent created"}

@router.get("/")
async def list_agents():
    return {"agents": []}

@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    return {"agent_id": agent_id}

@router.put("/{agent_id}")
async def update_agent(agent_id: str):
    return {"agent_id": agent_id}

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    return {"message": "Agent deleted"}
