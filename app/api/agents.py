from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.registry import registry

router = APIRouter()

class OwnerAction(BaseModel):
    owner_id: str

@router.get("")
def list_agents():
    return {"agents": registry.list_agents()}

@router.post("/{agent_id}/activate")
def activate(agent_id: str, action: OwnerAction):
    if action.owner_id != "owner-001":
        raise HTTPException(status_code=403, detail="Only Owner can activate agents.")
    return registry.set_status(agent_id, "ACTIVE", action.owner_id)

@router.post("/{agent_id}/deactivate")
def deactivate(agent_id: str, action: OwnerAction):
    if action.owner_id != "owner-001":
        raise HTTPException(status_code=403, detail="Only Owner can deactivate agents.")
    return registry.set_status(agent_id, "DISABLED", action.owner_id)
