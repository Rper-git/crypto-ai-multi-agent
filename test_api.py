import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['version']=='0.8.0'

def test_office():
    r=client.get('/api/office'); assert r.status_code==200; assert len(r.json()['agents'])==10

def test_chat():
    r=client.post('/api/chat',json={'message':'qual o risco atual?'}); assert r.status_code==200; assert 'Risk' in r.json()['reply']

def test_mission():
    r=client.post('/api/missions',json={'objective':'analisar BTC','capital':1000}); assert r.status_code==200; assert r.json()['decision']=='PAPER_ONLY'

def test_agent_action():
    r=client.post('/api/agents/action',json={'agent_id':'agent-04','action':'authorize_paper'}); assert r.status_code==200; assert r.json()['ok'] is True

def test_paper_buy_and_portfolio():
    r=client.post('/api/paper/order',json={'symbol':'BTC','side':'buy','qty':0.001,'price':100000}); assert r.status_code==200; assert r.json()['ok'] is True
    p=client.get('/api/portfolio'); assert p.status_code==200; assert len(p.json()['positions'])>=1
