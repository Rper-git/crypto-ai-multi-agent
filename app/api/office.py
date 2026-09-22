from fastapi import APIRouter
from pydantic import BaseModel
from app.services.office import advisor

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.get("/chat")
def chat_history():
    return {"messages": advisor.history()}

@router.post("/chat")
def chat(message: ChatMessage):
    answer = advisor.reply(message.message)
    return {"answer": answer, "messages": advisor.history()}
