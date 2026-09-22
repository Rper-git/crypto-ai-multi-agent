from datetime import datetime, timezone

class OfficeService:
    def __init__(self):
        self.messages = []
        self.broker = {"provider": None, "account_label": None, "mode": "PAPER", "status": "NOT_CONNECTED", "permissions": [], "connected_at": None, "note": "Credenciais reais não são persistidas nesta versão."}
        self.vacancies = [
            {"id":"role-01","title":"CIO / Investment Strategy","status":"OPEN","type":"AI Agent","skills":["asset allocation","portfolio construction","macroeconomics","risk budgeting","scenario analysis"],"mission":"Definir a estrutura de decisão de investimento e prioridades do escritório."},
            {"id":"role-02","title":"Quant Research","status":"OPEN","type":"AI Agent","skills":["Python","statistics","time series","backtesting","factor research","data analysis"],"mission":"Pesquisar hipóteses quantitativas e medir desempenho ajustado ao risco."},
            {"id":"role-03","title":"Portfolio & Risk Manager","status":"OPEN","type":"AI Agent","skills":["VaR","drawdown","position sizing","exposure limits","stress testing","risk/reward"],"mission":"Controlar risco, exposição e limites antes de qualquer decisão de execução."},
            {"id":"role-04","title":"Market Intelligence","status":"OPEN","type":"AI Agent","skills":["market data","news analysis","on-chain analytics","sentiment","event monitoring"],"mission":"Organizar informação de mercado e separar dados de ruído."},
            {"id":"role-05","title":"Execution & Treasury","status":"DRAFT","type":"AI Agent","skills":["order types","slippage","liquidity","fees","cash management","reconciliation"],"mission":"Preparar execução e tesouraria com limites definidos pelo Owner e Risk."},
            {"id":"role-06","title":"Compliance & Controls","status":"OPEN","type":"AI Agent","skills":["audit trail","KYC/AML concepts","policy controls","permissions","incident logging"],"mission":"Verificar controles, permissões, rastreabilidade e regras operacionais."},
        ]
    def now(self): return datetime.now(timezone.utc).isoformat()
    def connect_broker(self, provider, account_label, mode, permissions):
        self.broker.update({"provider":provider.strip() or None,"account_label":account_label.strip() or None,"mode":mode if mode in {"PAPER","READ_ONLY","LIVE"} else "PAPER","permissions":permissions,"status":"CONFIGURED","connected_at":self.now()})
        return self.broker
    def disconnect_broker(self):
        self.broker.update({"provider":None,"account_label":None,"status":"NOT_CONNECTED","permissions":[],"connected_at":None}); return self.broker
    def history(self): return self.messages
    def reply(self, message: str):
        text=message.strip(); low=text.lower()
        if not text: return "Escreva uma questão, expectativa ou ideia para o escritório."
        if any(k in low for k in ["corretora","broker","conta","api"]): answer="Antes de ligar uma conta real, devemos identificar a corretora, definir permissões mínimas e começar em modo PAPER ou READ_ONLY. Chaves e segredos devem ficar fora do código e ser armazenados em infraestrutura segura."
        elif any(k in low for k in ["riqueza","pouco","capital","investir"]): answer="O escritório pode trabalhar com um mandato de acumulação de longo prazo: contribuições pequenas e regulares, diversificação, controlo de custos, gestão de risco e limites de perda. Isto é uma estrutura de processo, não uma promessa de retorno."
        elif any(k in low for k in ["equipe","equipa","time","vaga","agente"]): answer="O Manager deve mapear lacunas de capacidade e propor vagas com missão, skills, permissões, risco e critérios de sucesso. O Owner aprova antes da ativação."
        elif any(k in low for k in ["relatório","report","resultado"]): answer="Os relatórios devem separar factos, dados, hipóteses, risco, decisões do Owner e desempenho observado. Nenhum relatório deve apresentar retorno futuro como garantido."
        else: answer="Registei a questão. Posso convertê-la em objetivo, tarefa, vaga, regra de governance ou requisito técnico do escritório."
        now=self.now(); self.messages.append({"role":"owner","message":text,"time":now}); self.messages.append({"role":"chief","message":answer,"time":now}); self.messages=self.messages[-60:]; return answer
    def reports(self):
        return [
            {"id":"rpt-001","title":"Daily Office Brief","period":"Hoje","status":"READY","summary":"Estado dos agentes, eventos e pendências de governance."},
            {"id":"rpt-002","title":"Risk & Exposure","period":"Último ciclo","status":"TEMPLATE","summary":"Estrutura para exposição, drawdown, concentração, limites e stress tests."},
            {"id":"rpt-003","title":"Research Pipeline","period":"Último ciclo","status":"TEMPLATE","summary":"Hipóteses, evidências, dados utilizados, backtests e próximos testes."},
            {"id":"rpt-004","title":"Performance Journal","period":"Mensal","status":"TEMPLATE","summary":"Registo de decisões e desempenho observado, separado de previsões."},
        ]
    def jobs(self): return self.vacancies
office=OfficeService()
