class ManagerAgent:
    """Agent 01 — central coordinator.

    The Manager can propose a new agent but cannot approve/create it autonomously.
    """

    agent_id = "agent-01"
    name = "Manager"

    def propose_new_agent(self, requested_agent, problem, why_existing_agents_are_insufficient,
                          expected_benefit, risks, complexity, required_permissions=None):
        return {
            "requested_agent": requested_agent,
            "problem": problem,
            "why_existing_agents_are_insufficient": why_existing_agents_are_insufficient,
            "expected_benefit": expected_benefit,
            "risks": risks,
            "complexity": complexity,
            "required_permissions": required_permissions or [],
            "status": "PENDING",
            "requires_owner_decision": True,
        }
