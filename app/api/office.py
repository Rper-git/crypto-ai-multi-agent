from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.office import office
router=APIRouter()
class ChatMessage(BaseModel): message:str=Field(min_length=1,max_length=2000)
class BrokerConfig(BaseModel):
    provider:str=Field(min_length=1,max_length=120); account_label:str=Field(min_length=1,max_length=120); mode:str="PAPER"; permissions:list[str]=[]
@router.get('/chat')
def chat_history(): return {'messages':office.history()}
@router.post('/chat')
def chat(message:ChatMessage): return {'answer':office.reply(message.message),'messages':office.history()}
@router.get('/broker')
def broker(): return office.broker
@router.post('/broker/configure')
def configure_broker(config:BrokerConfig): return office.connect_broker(config.provider,config.account_label,config.mode,config.permissions)
@router.post('/broker/disconnect')
def disconnect_broker(): return office.disconnect_broker()
@router.get('/reports')
def reports(): return {'reports':office.reports()}
@router.get('/jobs')
def jobs(): return {'jobs':office.jobs()}
