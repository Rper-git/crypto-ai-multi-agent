from datetime import datetime, timezone


class AgentRegistry:
    def __init__(self):
        self._agents = [
            {"id": "agent-01", "name": "Manager", "role": "orchestrator", "status": "ACTIVE", "description": "Coordena o escritório e reporta ao Owner."},
            {"id": "agent-02", "name": "Market Scanner", "role": "research", "status": "ACTIVE", "description": "Pesquisa dados e sinais de mercado."},
            {"id": "agent-03", "name": "Risk", "role": "risk", "status": "ACTIVE", "description": "Avalia risco, exposição e limites."},
            {"id": "agent-04", "name": "Executor", "role": "execution", "status": "DISABLED", "description": "Executa ordens quando explicitamente autorizado pelo Owner."},
        ]
        self._events = []

    def list_agents(self):
        return self._agents

    def get_agent(self, agent_id):
        return next((a for a in self._agents if a["id"] == agent_id), None)

    def set_status(self, agent_id, status, actor="owner-001"):
        agent = self.get_agent(agent_id)
        if not agent:
            raise KeyError("Agent not found")
        agent["status"] = status
        self._events.insert(0, {
            "time": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "actor": actor,
            "event": f"Estado alterado para {status}",
        })
        return agent

    def events(self):
        return self._events[:50]


registry = AgentRegistry()
