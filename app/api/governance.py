from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.governance import governance

router = APIRouter()

class AgentRequest(BaseModel):
    requested_agent: str
    problem: str
    why_existing_agents_are_insufficient: str
    expected_benefit: str
    risks: str
    complexity: str
    required_permissions: list[str] = []

@router.post("/agent-requests")
def create_request(request: AgentRequest):
    return governance.create_request(request.model_dump())

@router.get("/agent-requests")
def list_requests():
    return governance.list_requests()

@router.post("/agent-requests/{request_id}/approve")
def approve(request_id: str, owner_id: str):
    if owner_id != governance.owner_id:
        raise HTTPException(status_code=403, detail="Only Owner can approve.")
    return governance.decide(request_id, "APPROVED", owner_id)

@router.post("/agent-requests/{request_id}/reject")
def reject(request_id: str, owner_id: str):
    if owner_id != governance.owner_id:
        raise HTTPException(status_code=403, detail="Only Owner can reject.")
    return governance.decide(request_id, "REJECTED", owner_id)
