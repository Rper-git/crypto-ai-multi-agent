from app.services.governance import GovernanceService

def test_new_agent_request_requires_owner_decision():
    g = GovernanceService()
    r = g.create_request({
        "requested_agent": "Pattern Agent",
        "problem": "Detect chart patterns",
        "why_existing_agents_are_insufficient": "No existing agent performs this analysis",
        "expected_benefit": "Structured pattern detection",
        "risks": "False signals",
        "complexity": "Medium",
        "required_permissions": ["market_data"],
    })
    assert r["status"] == "PENDING"

def test_only_owner_can_decide():
    g = GovernanceService()
    r = g.create_request({
        "requested_agent": "Test Agent",
        "problem": "test",
        "why_existing_agents_are_insufficient": "test",
        "expected_benefit": "test",
        "risks": "test",
        "complexity": "Low",
    })
    try:
        g.decide(r["id"], "APPROVED", "not-owner")
        assert False
    except PermissionError:
        pass
