from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.registry import registry

router = APIRouter()

OWNER_ID = "owner-001"

class AgentControl(BaseModel):
    owner_id: str

@router.get("")
def list_agents():
    return {"agents": registry.list_agents()}

@router.get("/{agent_id}")
def get_agent(agent_id: str):
    agent = registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("/{agent_id}/activate")
def activate_agent(agent_id: str, control: AgentControl):
    if control.owner_id != OWNER_ID:
        raise HTTPException(status_code=403, detail="Only Owner can activate an agent.")
    agent = registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent_id != "agent-04":
        raise HTTPException(status_code=400, detail="This control is currently reserved for the Executor.")
    return {"ok": True, "agent": registry.set_status(agent_id, "ACTIVE", OWNER_ID)}

@router.post("/{agent_id}/deactivate")
def deactivate_agent(agent_id: str, control: AgentControl):
    if control.owner_id != OWNER_ID:
        raise HTTPException(status_code=403, detail="Only Owner can deactivate an agent.")
    agent = registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"ok": True, "agent": registry.set_status(agent_id, "DISABLED", OWNER_ID)}
