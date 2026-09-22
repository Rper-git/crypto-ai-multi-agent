from datetime import datetime, timezone


CURRENT_TEAM = [
    {
        "id": "agent-01",
        "name": "Manager",
        "title": "Gerente de Operações / Orquestrador",
        "role": "orchestrator",
        "status": "ACTIVE",
        "skills": ["orchestration", "task allocation", "governance", "reporting", "resource management"],
        "mission": "Supervisionar toda a equipe, distribuir tarefas, definir as diretrizes do ciclo e garantir que os setores operem em sintonia sob as regras do Owner.",
        "description": "Coordena o escritório e reporta ao Owner. Pode propor novos agentes, mas não pode aprová-los ou ativá-los sozinho.",
    },
    {
        "id": "agent-02",
        "name": "Market Scanner",
        "title": "Analisador de Mercado / Scanner",
        "role": "research",
        "status": "ACTIVE",
        "skills": ["market data", "price action", "liquidity", "pattern detection", "real-time monitoring"],
        "mission": "Varrer o mercado em busca de oportunidades, padrões de preço, liquidez e distorções, entregando observações ao Manager e ao Risk.",
        "description": "Pesquisa dados e sinais de mercado; não autoriza operações.",
    },
    {
        "id": "agent-03",
        "name": "Risk",
        "title": "Gerente de Risco / Risk Manager",
        "role": "risk",
        "status": "ACTIVE",
        "skills": ["position sizing", "exposure limits", "drawdown", "volatility", "stress testing", "stop-loss policy"],
        "mission": "Ser a barreira de proteção da operação: avaliar exposição, limites, volatilidade, tamanho de posição e condições de interrupção antes de qualquer execução.",
        "description": "Avalia risco e pode bloquear uma proposta que viole os limites definidos.",
    },
    {
        "id": "agent-04",
        "name": "Executor",
        "title": "Trader Executor",
        "role": "execution",
        "status": "DISABLED",
        "skills": ["order types", "slippage", "timing", "liquidity", "fees", "order management"],
        "mission": "Enviar e gerir ordens somente quando houver autorização explícita, respeitando limites de risco, permissões da conta e regras de Governance.",
        "description": "Execução permanece bloqueada por padrão e não deve operar uma conta real sem controlos adicionais.",
    },
]


class AgentRegistry:
    def __init__(self):
        self._agents = [dict(a) for a in CURRENT_TEAM]
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
