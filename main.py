from pathlib import Path
from typing import Optional
import json
import time
import uuid
import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE = Path(__file__).resolve().parent
app = FastAPI(title="Crypto AI Multi-Agent Trading Office", version="0.8.0")
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

activity_log = [
    {"id":"a1","agent":"Manager","text":"Escritório iniciado em modo seguro.","kind":"system"},
    {"id":"a2","agent":"Market Scanner","text":"A recolher cotações públicas.","kind":"market"},
    {"id":"a3","agent":"Risk","text":"A validar limites antes de qualquer simulação.","kind":"risk"},
    {"id":"a4","agent":"Executor","text":"Execução LIVE bloqueada por Governance.","kind":"blocked"},
]

paper = {"cash": 1250.0, "positions": [], "realized": 0.0}

async def fetch_market():
    symbols = list(FALLBACK)
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get("https://api.binance.com/api/v3/ticker/24hr", params={"symbols": json.dumps(symbols)})
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
    try:
        ids = "bitcoin,ethereum,solana,ripple,binancecoin,cardano"
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get("https://api.coingecko.com/api/v3/simple/price", params={"ids":ids,"vs_currencies":"usd","include_24hr_change":"true"})
            r.raise_for_status(); data=r.json()
        mapping={"bitcoin":"BTC","ethereum":"ETH","solana":"SOL","ripple":"XRP","binancecoin":"BNB","cardano":"ADA"}
        return [{"symbol":s,"price":float(data[k]["usd"]),"change":float(data[k].get("usd_24h_change",0)),"volume":0,"source":"CoinGecko"} for k,s in mapping.items()]
    except Exception:
        return [{**v,"source":"fallback"} for v in FALLBACK.values()]

def log(agent, text, kind="info"):
    activity_log.insert(0,{"id":uuid.uuid4().hex[:8],"agent":agent,"text":text,"kind":kind,"timestamp":int(time.time())})
    del activity_log[80:]

@app.get("/")
def root(): return FileResponse(BASE / "static" / "index.html")

@app.get("/health")
def health():
    return {"status":"online","version":"0.8.0","mode":"READ_ONLY + PAPER","live_trading":False,"timestamp":int(time.time())}

@app.get("/api/market")
async def market(): return {"updated_at":int(time.time()),"assets":await fetch_market()}

@app.get("/api/office")
def office(): return {"agents":AGENTS,"mode":"READ_ONLY + PAPER","live_trading":False,"updated_at":int(time.time())}

@app.get("/api/activity")
def activity(): return {"items":activity_log[:40]}

@app.get("/api/portfolio")
async def portfolio():
    assets = await fetch_market(); prices={a["symbol"]:a["price"] for a in assets}
    value=paper["cash"]; positions=[]
    for p in paper["positions"]:
        current=prices.get(p["symbol"],p["avg_price"])
        market_value=p["qty"]*current
        pnl=(current-p["avg_price"])*p["qty"]
        positions.append({**p,"current":current,"market_value":market_value,"pnl":pnl})
        value += market_value
    invested = 1250.0-paper["cash"]+sum(p["qty"]*p["avg_price"] for p in paper["positions"])
    # For the initial paper account, invested means deployed capital; cash remains part of total value.
    pnl=value-1250.0
    return {"connected":False,"broker":"Modo de teste","currency":"EUR","invested":round(max(invested,0),2),"value":round(value,2),"pnl":round(pnl,2),"pnl_pct":round(pnl/1250*100,2),"cash":round(paper["cash"],2),"positions":positions,"mode":"PAPER"}

@app.get("/api/reports")
def reports():
    return [
        {"id":"RPT-001","title":"Estado operacional","status":"OK","summary":"Manager, Scanner e Risk ativos. Executor permanece protegido por Governance."},
        {"id":"RPT-002","title":"Mercado","status":"LIVE DATA","summary":"Ticker obtido de fontes públicas com fallback automático."},
        {"id":"RPT-003","title":"Execução","status":"PAPER ONLY","summary":"Testes de ordens são simulados e não chegam à corretora."},
        {"id":"RPT-004","title":"Segurança","status":"PROTEGIDO","summary":"Nenhuma chave de corretora é guardada no frontend e trading LIVE está desativado."},
    ]

class ChatRequest(BaseModel): message: str = Field(min_length=1, max_length=2000)

@app.post("/api/chat")
def chat(req: ChatRequest):
    msg=req.message.lower(); log("Manager",f"Recebeu: {req.message}","chat")
    if "mercado" in msg or "cotação" in msg or "cotacoes" in msg:
        reply="Vou alinhar Scanner + Risk. O mercado está ligado a dados públicos; a análise continua informativa e sem execução LIVE."
        log("Manager","Solicitou análise conjunta de mercado ao Scanner e Risk.","mission")
    elif "risco" in msg:
        reply="O Risk mantém o bloqueio de execução LIVE. Para um teste, podemos usar PAPER TRADING e registrar exposição, stop lógico e motivo da decisão."
    elif "equipe" in msg or "equipa" in msg:
        reply="Há 4 posições preenchidas e 6 vagas estratégicas. O Owner continua com a palavra final sobre contratação e permissões."
    elif "executor" in msg:
        reply="O Executor está bloqueado para ordens LIVE. Ele pode participar de simulações PAPER quando o fluxo for autorizado pelo Manager."
    else:
        reply="Mensagem recebida. O Manager pode coordenar mercado, risco, equipa e simulações PAPER. O sistema continua sem envio de ordens reais."
    return {"speaker":"Manager","reply":reply,"timestamp":int(time.time())}

class MissionRequest(BaseModel):
    objective: str = Field(min_length=2, max_length=500)
    capital: float = Field(default=0, ge=0, le=1_000_000)

@app.post("/api/missions")
def mission(req: MissionRequest):
    cap=max(0,float(req.capital)); risk_limit=round(cap*0.01,2)
    log("Manager",f"Nova missão: {req.objective}","mission")
    log("Market Scanner","Mercado consultado em modo informativo.","market")
    log("Risk",f"Limite de risco de teste calculado: €{risk_limit:.2f}.","risk")
    return {"status":"completed","objective":req.objective,"capital":cap,"steps":[
        {"agent":"Manager","status":"completed","message":"Missão recebida e distribuída."},
        {"agent":"Market Scanner","status":"completed","message":"Mercado consultado em modo informativo."},
        {"agent":"Risk","status":"completed","message":f"Limite de risco de teste: €{risk_limit:.2f}."},
        {"agent":"Executor","status":"blocked","message":"LIVE bloqueado. Use PAPER para testar o fluxo."}],"decision":"PAPER_ONLY","timestamp":int(time.time())}

class AgentAction(BaseModel):
    agent_id: str
    action: str

@app.post("/api/agents/action")
def agent_action(req: AgentAction):
    allowed={"start","pause","block","authorize_paper"}
    if req.action not in allowed: return {"ok":False,"message":"Ação inválida."}
    agent=next((a for a in AGENTS if a["id"]==req.agent_id),None)
    if not agent: return {"ok":False,"message":"Agente não encontrado."}
    if agent["status"]=="vacancy": return {"ok":False,"message":"Esta posição ainda é uma vaga."}
    if req.action=="start":
        agent["status"]="working"; agent["activity"]="A trabalhar sob controlo do Owner."; log(agent["name"],"Agente colocado a trabalhar pelo Owner.","control")
    elif req.action=="pause":
        agent["status"]="idle"; agent["activity"]="Em espera por nova missão."; log(agent["name"],"Agente colocado em espera.","control")
    elif req.action=="block":
        agent["status"]="blocked"; agent["activity"]="Bloqueado pelo Owner/Governance."; log(agent["name"],"Agente bloqueado pelo Owner.","blocked")
    elif req.action=="authorize_paper":
        if agent["name"]!="Executor": return {"ok":False,"message":"A autorização PAPER só se aplica ao Executor."}
        agent["status"]="working"; agent["activity"]="PAPER autorizado. Nenhuma ordem LIVE será enviada."; log("Executor","PAPER autorizado pelo Owner; LIVE continua bloqueado.","control")
    return {"ok":True,"agent":agent}

class PaperOrder(BaseModel):
    symbol: str
    side: str
    qty: float = Field(gt=0)
    price: Optional[float] = Field(default=None, gt=0)

@app.post("/api/paper/order")
async def paper_order(req: PaperOrder):
    symbol=req.symbol.upper(); side=req.side.lower(); qty=float(req.qty)
    assets=await fetch_market(); found=next((a for a in assets if a["symbol"]==symbol),None)
    if not found: return {"ok":False,"message":"Ativo não disponível no ticker."}
    price=float(req.price or found["price"]); cost=qty*price
    if side=="buy":
        if paper["cash"]<cost: return {"ok":False,"message":"Saldo PAPER insuficiente."}
        paper["cash"]-=cost
        existing=next((p for p in paper["positions"] if p["symbol"]==symbol),None)
        if existing:
            total_qty=existing["qty"]+qty; existing["avg_price"]=(existing["qty"]*existing["avg_price"]+cost)/total_qty; existing["qty"]=total_qty
        else: paper["positions"].append({"symbol":symbol,"qty":qty,"avg_price":price})
        log("Executor",f"PAPER BUY {qty:g} {symbol} a {price:g}.","paper")
    elif side=="sell":
        existing=next((p for p in paper["positions"] if p["symbol"]==symbol),None)
        if not existing or existing["qty"]<qty: return {"ok":False,"message":"Posição PAPER insuficiente."}
        paper["cash"]+=cost; paper["realized"]+=(price-existing["avg_price"])*qty; existing["qty"]-=qty
        if existing["qty"]<=1e-12: paper["positions"].remove(existing)
        log("Executor",f"PAPER SELL {qty:g} {symbol} a {price:g}.","paper")
    else: return {"ok":False,"message":"Side deve ser buy ou sell."}
    return {"ok":True,"mode":"PAPER","symbol":symbol,"side":side,"qty":qty,"price":price,"timestamp":int(time.time())}
