from datetime import datetime, timezone
from uuid import uuid4
from app.services.registry import registry

class WorkflowService:
    """Deterministic end-to-end office test workflow.

    It simulates research/risk coordination without real market data or order execution.
    This is intentionally safe for testing the multi-agent architecture.
    """
    def __init__(self):
        self.missions = []

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def run_test_cycle(self, objective: str, capital: float | None = None):
        objective = objective.strip() or "Testar o processo de pesquisa e controlo de risco."
        capital = float(capital or 100.0)
        if capital <= 0:
            raise ValueError("Capital de teste deve ser maior que zero.")

        mission = {
            "id": str(uuid4()),
            "objective": objective,
            "capital": capital,
            "mode": "SIMULATION",
            "started_at": self._now(),
            "status": "RUNNING",
            "steps": [],
            "final_decision": None,
        }
        self.missions.insert(0, mission)

        self._step(mission, "Manager", "Recebeu a missão e dividiu o trabalho entre pesquisa e risco.", "DONE")
        self._step(mission, "Market Scanner", "Analisou um conjunto de dados sintético para validar o fluxo de pesquisa.", "DONE", {
            "universe": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
            "signal": "OBSERVATION_ONLY",
            "data_source": "synthetic_test_data",
            "finding": "Nenhuma ordem é criada nesta simulação.",
        })

        risk = {
            "max_test_allocation": round(capital * 0.10, 2),
            "max_single_position": round(capital * 0.05, 2),
            "leverage": 0,
            "live_execution": False,
            "result": "PASS_WITH_CAUTION",
        }
        self._step(mission, "Risk", "Aplicou limites de teste e bloqueou alavancagem/execução real.", "DONE", risk)

        final = {
            "decision": "NO_LIVE_TRADE",
            "reason": "O ciclo é de simulação; os dados são sintéticos e o Executor não envia ordens reais.",
            "next_action": "Repetir com dados reais em READ_ONLY/PAPER antes de qualquer modo LIVE.",
        }
        self._step(mission, "Manager", "Consolidou as respostas e preparou o relatório para o Owner.", "DONE", final)
        mission["final_decision"] = final
        mission["status"] = "COMPLETED"
        mission["finished_at"] = self._now()

        registry.add_event("workflow", "Owner", f"Ciclo de teste concluído: {mission['id']}")
        return mission

    def _step(self, mission, agent_name, action, status, output=None):
        mission["steps"].append({
            "id": str(uuid4()),
            "agent": agent_name,
            "action": action,
            "status": status,
            "output": output or {},
            "time": self._now(),
        })

    def list_missions(self):
        return self.missions[:20]

workflow = WorkflowService()
