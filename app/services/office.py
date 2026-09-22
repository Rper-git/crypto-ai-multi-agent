from datetime import datetime, timezone


class OfficeAdvisor:
    """Chat local de V0.3 para alinhar o escritório.

    É deliberadamente determinístico: ainda não chama um LLM externo.
    Na próxima versão poderá ser ligado a um modelo com memória e ferramentas.
    """
    def __init__(self):
        self.messages = []

    def reply(self, message: str):
        text = message.strip()
        low = text.lower()
        if not text:
            return "Escreva uma questão, expectativa ou ideia para o escritório."

        if any(k in low for k in ["executor", "executar", "ordem", "trade"]):
            answer = "O Executor continua sob controlo do Owner. Antes de execução real, precisamos definir limites, permissões, risco e modo de aprovação."
        elif any(k in low for k in ["equipe", "equipa", "time", "agentes"]):
            answer = "O Manager deve coordenar a equipa, medir lacunas de capacidade e apresentar pedidos fundamentados ao Owner. Cada novo agente deve ter missão, permissões e critérios de ativação."
        elif any(k in low for k in ["ideia", "ideias", "expectativa", "objetivo", "meta"]):
            answer = "Podemos transformar a ideia em um objetivo operacional: resultado esperado, responsável, dados necessários, risco, critérios de sucesso e aprovação do Owner."
        elif any(k in low for k in ["desenvolvimento", "desenvolver", "próximo", "proxima", "próxima"]):
            answer = "Sugestão de alinhamento: primeiro consolidar estado e comunicação dos agentes; depois ligar modelos e dados reais; por último habilitar execução apenas com governance e limites verificáveis."
        else:
            answer = "Registei a questão. O próximo passo é convertê-la em uma decisão, tarefa ou pedido de capacidade para o escritório."

        now = datetime.now(timezone.utc).isoformat()
        self.messages.append({"role": "owner", "message": text, "time": now})
        self.messages.append({"role": "chief", "message": answer, "time": now})
        self.messages = self.messages[-40:]
        return answer

    def history(self):
        return self.messages


advisor = OfficeAdvisor()
