from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_routes():
    for path in ['/', '/health', '/dashboard', '/office/broker', '/office/reports', '/office/jobs']:
        assert client.get(path).status_code==200
def test_broker_config():
    r=client.post('/office/broker/configure',json={'provider':'Demo Broker','account_label':'Paper','mode':'PAPER','permissions':['market_data']})
    assert r.status_code==200 and r.json()['status']=='CONFIGURED'
