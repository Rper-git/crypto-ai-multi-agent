from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.workflow import workflow

router = APIRouter()

class TestMission(BaseModel):
    objective: str = Field(min_length=3, max_length=500)
    capital: float = Field(default=100.0, gt=0, le=1_000_000)

@router.post('/test-cycle')
def test_cycle(mission: TestMission):
    try:
        return workflow.run_test_cycle(mission.objective, mission.capital)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.get('/missions')
def missions():
    return {"missions": workflow.list_missions()}
