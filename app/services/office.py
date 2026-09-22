from datetime import datetime, timezone


class OfficeService:
    def __init__(self):
        self.messages = []
        self.broker = {
            "provider": None,
            "account_label": None,
            "mode": "PAPER",
            "status": "NOT_CONNECTED",
            "permissions": [],
            "connected_at": None,
            "note": "Credenciais reais não são persistidas nesta versão.",
        }
        # Vagas para as funções que ainda não fazem parte da equipe atual.
        self.vacancies = [
            {"id":"role-01","title":"Estrategista-Chefe (Chief Investment Officer)","status":"OPEN","type":"AI Agent","skills":["asset allocation","portfolio construction","macroeconomics","investment thesis","scenario analysis"],"mission":"Definir a tese global de investimentos, prioridades por classe de ativo e hipóteses estratégicas para o escritório."},
            {"id":"role-02","title":"Analista Fundamentalista","status":"OPEN","type":"AI Agent","skills":["financial statements","valuation","fundamental analysis","macroeconomics","company research"],"mission":"Avaliar a saúde financeira e económica dos ativos, identificar riscos fundamentais e separar qualidade de especulação."},
            {"id":"role-03","title":"Analista de Sentimento de Mercado","status":"OPEN","type":"AI Agent","skills":["news analysis","sentiment analysis","social signals","event monitoring","NLP"],"mission":"Monitorizar notícias, sentimento e eventos para identificar mudanças de narrativa e possíveis fontes de volatilidade."},
            {"id":"role-04","title":"Analista de Liquidez e Colateral","status":"OPEN","type":"AI Agent","skills":["liquidity monitoring","margin","collateral","cash management","stress testing"],"mission":"Monitorizar liquidez, caixa e colateral e sinalizar riscos de margem ou de incapacidade de cumprir obrigações."},
            {"id":"role-05","title":"Auditor de Compliance / Conformidade","status":"OPEN","type":"AI Agent","skills":["audit trail","permissions","policy controls","KYC/AML concepts","incident logging"],"mission":"Verificar conformidade, permissões, rastreabilidade e regras operacionais antes e depois das decisões críticas."},
            {"id":"role-06","title":"Especialista em Arbitragem","status":"OPEN","type":"AI Agent","skills":["cross-venue pricing","market microstructure","fees","slippage","execution risk"],"mission":"Pesquisar diferenças de preço entre mercados e avaliar oportunidades de arbitragem considerando taxas, latência, liquidez e risco de execução."},
        ]

    def now(self):
        return datetime.now(timezone.utc).isoformat()

    def connect_broker(self, provider, account_label, mode, permissions):
        self.broker.update({
            "provider": provider.strip() or None,
            "account_label": account_label.strip() or None,
            "mode": mode if mode in {"PAPER", "READ_ONLY", "LIVE"} else "PAPER",
            "permissions": permissions,
            "status": "CONFIGURED",
            "connected_at": self.now(),
        })
        return self.broker

    def disconnect_broker(self):
        self.broker.update({"provider":None,"account_label":None,"status":"NOT_CONNECTED","permissions":[],"connected_at":None})
        return self.broker

    def history(self):
        return self.messages

    def reply(self, message: str):
        text = message.strip()
        low = text.lower()
        if not text:
            return "Escreva uma questão, expectativa ou ideia para o escritório."
        if any(k in low for k in ["corretora", "broker", "conta", "api"]):
            answer = "Antes de ligar uma conta real, devemos identificar a corretora, definir permissões mínimas e começar em modo PAPER ou READ_ONLY. Chaves e segredos devem ficar fora do código e ser armazenados em infraestrutura segura."
        elif any(k in low for k in ["riqueza", "pouco", "capital", "investir"]):
            answer = "O escritório pode trabalhar com um mandato de acumulação de longo prazo: contribuições pequenas e regulares, diversificação, controlo de custos, gestão de risco e disciplina. Isto é uma estrutura de processo, não uma promessa de retorno."
        elif any(k in low for k in ["equipe", "equipa", "time", "vaga", "agente"]):
            answer = "A equipe atual tem Manager, Market Scanner, Risk e Executor. O Manager deve mapear lacunas e propor novas vagas com missão, skills, permissões, risco e critérios de sucesso. O Owner aprova antes da ativação."
        elif any(k in low for k in ["relatório", "report", "resultado"]):
            answer = "Os relatórios devem separar factos, dados, hipóteses, risco, decisões do Owner e desempenho observado. Nenhum relatório deve apresentar retorno futuro como garantido."
        else:
            answer = "Registei a questão. Posso convertê-la em objetivo, tarefa, vaga, regra de governance ou requisito técnico do escritório."
        now = self.now()
        self.messages.append({"role":"owner","message":text,"time":now})
        self.messages.append({"role":"chief","message":answer,"time":now})
        self.messages = self.messages[-60:]
        return answer

    def reports(self):
        return [
            {"id":"rpt-001","title":"Daily Office Brief","period":"Hoje","status":"READY","summary":"Estado dos agentes, eventos, tarefas e pendências de governance."},
            {"id":"rpt-002","title":"Risk & Exposure","period":"Último ciclo","status":"TEMPLATE","summary":"Exposição, drawdown, concentração, volatilidade, limites e stress tests."},
            {"id":"rpt-003","title":"Research Pipeline","period":"Último ciclo","status":"TEMPLATE","summary":"Hipóteses, evidências, dados utilizados, backtests e próximos testes."},
            {"id":"rpt-004","title":"Performance Journal","period":"Mensal","status":"TEMPLATE","summary":"Registo de decisões, resultados observados, custos e desvios ao mandato."},
        ]

    def jobs(self):
        return self.vacancies


office = OfficeService()
