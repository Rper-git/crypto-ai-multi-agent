from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_end_to_end_test_cycle():
    r = client.post('/office/test-cycle', json={
        'objective': 'Testar o escritório com capital pequeno',
        'capital': 100,
    })
    assert r.status_code == 200
    data = r.json()
    assert data['status'] == 'COMPLETED'
    assert data['mode'] == 'SIMULATION'
    assert data['final_decision']['decision'] == 'NO_LIVE_TRADE'
    assert [s['agent'] for s in data['steps']] == ['Manager', 'Market Scanner', 'Risk', 'Manager']


def test_missions_endpoint():
    r = client.get('/office/missions')
    assert r.status_code == 200
    assert 'missions' in r.json()


def test_health_is_v06():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['version'] == '0.6.0'
