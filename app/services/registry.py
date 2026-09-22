class AgentRegistry:
    def __init__(self):
        self._agents = [
            {"id": "agent-01", "name": "Manager", "role": "orchestrator", "status": "ACTIVE"},
            {"id": "agent-02", "name": "Market Scanner", "role": "research", "status": "ACTIVE"},
            {"id": "agent-03", "name": "Risk", "role": "risk", "status": "ACTIVE"},
            {"id": "agent-04", "name": "Executor", "role": "execution", "status": "DISABLED"},
        ]

    def list_agents(self):
        return self._agents

registry = AgentRegistry()
