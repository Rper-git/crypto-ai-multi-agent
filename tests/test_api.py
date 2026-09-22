from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['version']=='0.7.0'

def test_office():
    r=client.get('/api/office'); assert r.status_code==200; assert len(r.json()['agents'])==10

def test_mission_blocks_live():
    r=client.post('/api/missions',json={'objective':'teste','capital':100}); assert r.status_code==200; assert r.json()['decision']=='NO_LIVE_TRADE'

def test_chat():
    r=client.post('/api/chat',json={'message':'qual o risco?'}); assert r.status_code==200; assert 'bloqueada' in r.json()['reply']
