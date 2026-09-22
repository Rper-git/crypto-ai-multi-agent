from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_team_has_four_current_agents_and_missions():
    data = client.get('/agents').json()['agents']
    assert len(data) == 4
    assert all(a['mission'] for a in data)
    assert data[0]['title'].startswith('Gerente')
    assert data[3]['title'] == 'Trader Executor'

def test_owner_can_activate_executor_and_non_owner_cannot():
    bad = client.post('/agents/agent-04/activate', json={'owner_id':'wrong'} )
    assert bad.status_code == 403
    good = client.post('/agents/agent-04/activate', json={'owner_id':'owner-001'})
    assert good.status_code == 200
    assert good.json()['status'] == 'ACTIVE'

def test_financial_vacancies_match_team_plan():
    jobs = client.get('/office/jobs').json()['jobs']
    titles = [j['title'] for j in jobs]
    assert 'Estrategista-Chefe (Chief Investment Officer)' in titles
    assert 'Analista Fundamentalista' in titles
    assert 'Analista de Sentimento de Mercado' in titles
    assert 'Analista de Liquidez e Colateral' in titles
    assert 'Auditor de Compliance / Conformidade' in titles
    assert 'Especialista em Arbitragem' in titles
