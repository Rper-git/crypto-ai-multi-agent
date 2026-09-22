from pathlib import Path
from typing import Optional
import time
import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE = Path(__file__).resolve().parent
app = FastAPI(title="Crypto AI Multi-Agent Trading Office", version="0.7.0")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

AGENTS = [
    {"id":"agent-01","name":"Manager","role":"Orquestrador","mission":"Supervisionar a equipa e distribuir missões.","status":"working","activity":"A organizar o ciclo de análise.","skill":92,"desk":1},
    {"id":"agent-02","name":"Market Scanner","role":"Analista de Mercado","mission":"Detetar movimentos, liquidez e oportunidades no mercado.","status":"working","activity":"A recolher cotações e movimentos.","skill":88,"desk":2},
    {"id":"agent-03","name":"Risk","role":"Gestor de Risco","mission":"Controlar exposição, volatilidade e limites de risco.","status":"working","activity":"A validar risco do cenário atual.","skill":95,"desk":3},
    {"id":"agent-04","name":"Executor","role":"Trader Executor","mission":"Executar ordens apenas com autorização e controlos aprovados.","status":"blocked","activity":"Bloqueado: modo LIVE desativado.","skill":86,"desk":4},
    {"id":"agent-05","name":"CIO","role":"Estrategista-Chefe","mission":"Definir teses e alocação estratégica.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":5},
    {"id":"agent-06","name":"Fundamentalista","role":"Analista Fundamentalista","mission":"Avaliar qualidade financeira e valuation.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":6},
    {"id":"agent-07","name":"Sentimento","role":"Analista de Sentimento","mission":"Monitorizar notícias e sentimento do mercado.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":7},
    {"id":"agent-08","name":"Liquidez","role":"Liquidez & Colateral","mission":"Controlar liquidez, margem e colateral.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":8},
    {"id":"agent-09","name":"Compliance","role":"Auditor de Compliance","mission":"Garantir regras, permissões e rastreabilidade.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":9},
    {"id":"agent-10","name":"Arbitragem","role":"Especialista em Arbitragem","mission":"Pesquisar diferenças de preço considerando custos e execução.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":10},
]

FALLBACK = {
    "BTCUSDT":{"symbol":"BTC","price":104235.0,"change":2.31,"volume":0},
    "ETHUSDT":{"symbol":"ETH","price":3842.0,"change":-0.82,"volume":0},
    "SOLUSDT":{"symbol":"SOL","price":241.0,"change":4.18,"volume":0},
    "XRPUSDT":{"symbol":"XRP","price":2.91,"change":1.73,"volume":0},
    "BNBUSDT":{"symbol":"BNB","price":651.0,"change":-0.34,"volume":0},
    "ADAUSDT":{"symbol":"ADA","price":0.82,"change":0.91,"volume":0},
}

async def fetch_market():
    symbols = list(FALLBACK)
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, params={"symbols": __import__('json').dumps(symbols)})
            r.raise_for_status()
            rows = r.json()
        out=[]
        for row in rows:
            key=row["symbol"]
            if key in FALLBACK:
                out.append({"symbol":FALLBACK[key]["symbol"],"price":float(row["lastPrice"]),"change":float(row["priceChangePercent"]),"volume":float(row["quoteVolume"]),"source":"Binance"})
        if out:
            return out
    except Exception:
        pass
    return [{**v,"source":"fallback"} for v in FALLBACK.values()]

@app.get("/")
def root():
    return FileResponse(BASE / "static" / "index.html")

@app.get("/health")
def health():
    return {"status":"online","version":"0.7.0","mode":"READ_ONLY","timestamp":int(time.time())}

@app.get("/api/market")
async def market():
    return {"updated_at":int(time.time()),"assets":await fetch_market()}

@app.get("/api/office")
def office():
    return {"agents":AGENTS,"mode":"READ_ONLY","live_trading":False,"updated_at":int(time.time())}

@app.get("/api/portfolio")
def portfolio():
    return {"connected":False,"broker":"Não conectada","currency":"EUR","invested":0,"value":0,"pnl":0,"pnl_pct":0,"cash":0,"positions":[]}

@app.get("/api/reports")
def reports():
    return [{"id":"RPT-001","title":"Estado operacional","status":"OK","summary":"Equipe inicial ativa em modo de teste e execução LIVE bloqueada."},{"id":"RPT-002","title":"Risco","status":"PROTEGIDO","summary":"Nenhuma ordem real autorizada; corretora ainda não conectada."}]

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def chat(req: ChatRequest):
    msg=req.message.lower()
    if "mercado" in msg or "cotação" in msg or "cotacoes" in msg:
        reply="Vou alinhar o Scanner e o Risk. O painel está a usar cotações públicas de mercado em modo READ_ONLY; nenhuma ordem real será enviada."
    elif "risco" in msg:
        reply="O Risk mantém a execução LIVE bloqueada. Antes de qualquer operação real, precisamos de limites, fonte de dados, regras de exposição e aprovação do Owner."
    elif "equipe" in msg or "equipa" in msg:
        reply="Neste momento existem 4 agentes registados e 6 vagas estratégicas abertas. Posso estruturar as próximas contratações por função e skills."
    else:
        reply="Mensagem recebida. O Manager vai coordenar a análise com os agentes adequados. Este ambiente continua em modo READ_ONLY."
    return {"speaker":"Manager","reply":reply,"timestamp":int(time.time())}

class MissionRequest(BaseModel):
    objective: str
    capital: float = 0

@app.post("/api/missions")
def mission(req: MissionRequest):
    cap=max(0,float(req.capital))
    risk_limit=round(cap*0.01,2)
    return {"status":"completed","objective":req.objective,"capital":cap,"steps":[
        {"agent":"Manager","status":"completed","message":"Missão recebida e distribuída."},
        {"agent":"Market Scanner","status":"completed","message":"Mercado consultado em modo informativo."},
        {"agent":"Risk","status":"completed","message":f"Limite de risco de teste sugerido: €{risk_limit:.2f}."},
        {"agent":"Executor","status":"blocked","message":"Execução LIVE permanece bloqueada por Governance."}],"decision":"NO_LIVE_TRADE","timestamp":int(time.time())}
