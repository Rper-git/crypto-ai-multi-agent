class ExecutorAgent:
    agent_id = "agent-04"
    name = "Executor"

    # V0.1 intentionally contains no real broker execution.
    def execute(self, signal):
        raise NotImplementedError("Real trading execution is disabled in V0.1.")
