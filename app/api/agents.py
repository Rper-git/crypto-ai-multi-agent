from fastapi import APIRouter
from app.services.registry import registry

router = APIRouter()

@router.get("")
def list_agents():
    return {"agents": registry.list_agents()}
