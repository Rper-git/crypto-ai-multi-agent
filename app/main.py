from pathlib import Path
from typing import Optional
import base64
import hashlib
import hmac
import json
import os
import time
import uuid
import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE = Path(__file__).resolve().parent
VERSION = "0.9.0"
app = FastAPI(title="Crypto AI Multi-Agent Trading Office", version=VERSION)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

AGENTS = [
    {"id":"agent-01","name":"Manager","role":"Orquestrador","mission":"Supervisionar a equipa e distribuir missões.","status":"working","activity":"A organizar o ciclo de análise.","skill":92,"desk":1},
    {"id":"agent-02","name":"Market Scanner","role":"Analista de Mercado","mission":"Detetar movimentos, liquidez e oportunidades.","status":"working","activity":"A recolher cotações e movimentos.","skill":88,"desk":2},
    {"id":"agent-03","name":"Risk","role":"Gestor de Risco","mission":"Controlar exposição, volatilidade e limites.","status":"working","activity":"A validar risco do cenário atual.","skill":95,"desk":3},
    {"id":"agent-04","name":"Executor","role":"Trader Executor","mission":"Executar ordens apenas após aprovação do Owner.","status":"blocked","activity":"A aguardar autorização do Owner.","skill":86,"desk":4},
    {"id":"agent-05","name":"CIO","role":"Estrategista-Chefe","mission":"Definir teses e alocação estratégica.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":5},
    {"id":"agent-06","name":"Fundamentalista","role":"Analista Fundamentalista","mission":"Avaliar qualidade financeira e valuation.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":6},
    {"id":"agent-07","name":"Sentimento","role":"Analista de Sentimento","mission":"Monitorizar notícias e sentimento.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":7},
    {"id":"agent-08","name":"Liquidez","role":"Liquidez & Colateral","mission":"Controlar caixa, margem e colateral.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":8},
    {"id":"agent-09","name":"Compliance","role":"Auditor de Compliance","mission":"Garantir regras e rastreabilidade.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":9},
    {"id":"agent-10","name":"Arbitragem","role":"Especialista em Arbitragem","mission":"Pesquisar diferenças de preço após custos.","status":"vacancy","activity":"Vaga aberta.","skill":0,"desk":10},
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
    {"id":"a1","agent":"Manager","text":"Escritório iniciado. A coordenar o ciclo de análise.","kind":"system","timestamp":int(time.time())},
    {"id":"a2","agent":"Market Scanner","text":"A recolher cotações públicas em tempo real.","kind":"market","timestamp":int(time.time())},
    {"id":"a3","agent":"Risk","text":"A validar exposição antes de qualquer ordem.","kind":"risk","timestamp":int(time.time())},
    {"id":"a4","agent":"Executor","text":"Execução real protegida por Governance.","kind":"blocked","timestamp":int(time.time())},
]
paper = {"cash": 1250.0, "positions": [], "realized": 0.0}

async def fetch_market():
    symbols = list(FALLBACK)
    try:
        async with httpx.AsyncClient(timeout=6) as client:
            r = await client.get("https://api.binance.com/api/v3/ticker/24hr", params={"symbols": json.dumps(symbols)})
            r.raise_for_status()
            rows = r.json()
        out=[]
        for row in rows:
            key=row["symbol"]
            if key in FALLBACK:
                out.append({"symbol":FALLBACK[key]["symbol"],"price":float(row["lastPrice"]),"change":float(row["priceChangePercent"]),"volume":float(row["quoteVolume"]),"source":"Binance"})
        if out:
            return sorted(out, key=lambda x: ["BTC","ETH","SOL","XRP","BNB","ADA"].index(x["symbol"]))
    except Exception:
        pass
    try:
        ids = "bitcoin,ethereum,solana,ripple,binancecoin,cardano"
        async with httpx.AsyncClient(timeout=6) as client:
            r = await client.get("https://api.coingecko.com/api/v3/simple/price", params={"ids":ids,"vs_currencies":"usd","include_24hr_change":"true"})
            r.raise_for_status(); data=r.json()
        mapping={"bitcoin":"BTC","ethereum":"ETH","solana":"SOL","ripple":"XRP","binancecoin":"BNB","cardano":"ADA"}
        return [{"symbol":s,"price":float(data[k]["usd"]),"change":float(data[k].get("usd_24h_change",0)),"volume":0,"source":"CoinGecko"} for k,s in mapping.items() if k in data]
    except Exception:
        return [{**v,"source":"fallback"} for v in FALLBACK.values()]

def log(agent, text, kind="info"):
    activity_log.insert(0,{"id":uuid.uuid4().hex[:8],"agent":agent,"text":text,"kind":kind,"timestamp":int(time.time())})
    del activity_log[80:]

@app.get("/")
def root(): return FileResponse(BASE / "static" / "index.html")

@app.get("/health")
def health():
    return {"status":"online","version":VERSION,"mode":"READ_ONLY + PAPER","live_trading":False,"openai_configured":bool(os.getenv("OPENAI_API_KEY")),"timestamp":int(time.time())}

@app.get("/api/market")
async def market(): return {"updated_at":int(time.time()),"assets":await fetch_market()}

@app.get("/api/office")
def office(): return {"agents":AGENTS,"mode":"READ_ONLY + PAPER","live_trading":False,"updated_at":int(time.time())}

@app.get("/api/activity")
def activity(): return {"items":activity_log[:50]}

@app.get("/api/portfolio")
async def portfolio():
    assets = await fetch_market(); prices={a["symbol"]:a["price"] for a in assets}
    value=paper["cash"]; positions=[]
    for p in paper["positions"]:
        current=prices.get(p["symbol"],p["avg_price"]); market_value=p["qty"]*current; pnl=(current-p["avg_price"])*p["qty"]
        positions.append({**p,"current":current,"market_value":market_value,"pnl":pnl}); value += market_value
    invested = 1250.0-paper["cash"]+sum(p["qty"]*p["avg_price"] for p in paper["positions"])
    pnl=value-1250.0
    return {"connected":False,"broker":"Modo PAPER","currency":"EUR","invested":round(max(invested,0),2),"value":round(value,2),"pnl":round(pnl,2),"pnl_pct":round(pnl/1250*100,2),"cash":round(paper["cash"],2),"positions":positions,"mode":"PAPER"}

@app.get("/api/reports")
def reports():
    return [
        {"id":"RPT-001","title":"Estado operacional","status":"OK","summary":"Manager, Scanner e Risk ativos; Executor protegido por Governance."},
        {"id":"RPT-002","title":"Mercado","status":"LIVE DATA","summary":"Ticker público com fallback automático."},
        {"id":"RPT-003","title":"Execução","status":"PAPER ONLY","summary":"O fluxo de investimento é simulado até a conexão e aprovação do Owner."},
        {"id":"RPT-004","title":"IA","status":"READY" if os.getenv("OPENAI_API_KEY") else "CONFIGURAR","summary":"O Chat pode usar OpenAI no backend sem expor a chave ao navegador."},
    ]

class ChatRequest(BaseModel): message: str = Field(min_length=1, max_length=4000)

async def openai_chat(message: str):
    key=os.getenv("OPENAI_API_KEY")
    if not key: return None
    model=os.getenv("OPENAI_MODEL","gpt-5")
    system=("És o Manager de um escritório privado de análise de criptoativos. "
            "Coordena Scanner, Risk, CIO e Executor. Dá análise factual, explica riscos, "
            "não prometas lucros e nunca assumes que uma ordem real foi executada. "
            "Quando faltarem dados, pede-os. Responde em português de Portugal, de forma concisa.")
    payload={"model":model,"input":[{"role":"system","content":[{"type":"input_text","text":system}]},{"role":"user","content":[{"type":"input_text","text":message}]}]}
    async with httpx.AsyncClient(timeout=25) as client:
        r=await client.post("https://api.openai.com/v1/responses",headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},json=payload)
        r.raise_for_status(); data=r.json()
    text=data.get("output_text")
    if text: return text
    chunks=[]
    for item in data.get("output",[]):
        for c in item.get("content",[]):
            if isinstance(c,dict) and c.get("text"): chunks.append(c["text"])
    return "\n".join(chunks) or "Não foi possível obter resposta do modelo."

@app.post("/api/chat")
async def chat(req: ChatRequest):
    log("Manager",f"Recebeu: {req.message}","chat")
    try:
        ai=await openai_chat(req.message)
        if ai:
            log("Manager","Resposta produzida por OpenAI.","ai")
            return {"speaker":"Manager / OpenAI","reply":ai,"provider":"OpenAI","timestamp":int(time.time())}
    except Exception as exc:
        log("Manager",f"OpenAI indisponível; fallback local ({type(exc).__name__}).","warning")
    msg=req.message.lower()
    if "mercado" in msg or "cotação" in msg or "cotacoes" in msg:
        reply="Vou alinhar Scanner + Risk. Os preços vêm de dados públicos; a análise não significa recomendação nem execução automática."
    elif "risco" in msg:
        reply="O Risk deve validar exposição, liquidez e limites antes de qualquer operação. O ambiente atual continua PAPER."
    elif "equipe" in msg or "equipa" in msg:
        reply="Existem 4 funções preenchidas e 6 vagas. O Owner mantém a decisão final sobre novas contratações e permissões."
    elif "executor" in msg:
        reply="O Executor está preparado para PAPER, mas ordens reais continuam desativadas nesta versão."
    else:
        reply="Mensagem recebida. Posso coordenar mercado, risco, equipa e simulações PAPER. Configure OPENAI_API_KEY para ligar o Chat ao modelo."
    return {"speaker":"Manager","reply":reply,"provider":"local","timestamp":int(time.time())}

class MissionRequest(BaseModel):
    objective: str = Field(min_length=2, max_length=500)
    capital: float = Field(default=0, ge=0, le=1_000_000)

@app.post("/api/missions")
def mission(req: MissionRequest):
    cap=max(0,float(req.capital)); risk_limit=round(cap*0.01,2)
    log("Manager",f"Nova missão: {req.objective}","mission"); log("Market Scanner","Mercado consultado.","market"); log("Risk",f"Limite de risco de teste: €{risk_limit:.2f}.","risk")
    return {"status":"completed","objective":req.objective,"capital":cap,"steps":[{"agent":"Manager","status":"completed","message":"Missão recebida e distribuída."},{"agent":"Market Scanner","status":"completed","message":"Mercado consultado."},{"agent":"Risk","status":"completed","message":f"Limite de risco de teste: €{risk_limit:.2f}."},{"agent":"Executor","status":"blocked","message":"LIVE permanece bloqueado; o fluxo PAPER está disponível."}],"decision":"PAPER_ONLY","timestamp":int(time.time())}

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
    if req.action=="start": agent["status"]="working"; agent["activity"]="A trabalhar sob controlo do Owner."; log(agent["name"],"Agente colocado a trabalhar pelo Owner.","control")
    elif req.action=="pause": agent["status"]="idle"; agent["activity"]="Em espera por nova missão."; log(agent["name"],"Agente colocado em espera.","control")
    elif req.action=="block": agent["status"]="blocked"; agent["activity"]="Bloqueado pelo Owner/Governance."; log(agent["name"],"Agente bloqueado pelo Owner.","blocked")
    elif req.action=="authorize_paper":
        if agent["name"]!="Executor": return {"ok":False,"message":"A autorização PAPER só se aplica ao Executor."}
        agent["status"]="working"; agent["activity"]="PAPER autorizado. LIVE continua bloqueado."; log("Executor","PAPER autorizado pelo Owner; LIVE continua bloqueado.","control")
    return {"ok":True,"agent":agent}

class PaperOrder(BaseModel):
    symbol: str
    side: str
    qty: float = Field(gt=0)
    price: Optional[float] = Field(default=None, gt=0)

@app.post("/api/paper/order")
async def paper_order(req: PaperOrder):
    symbol=req.symbol.upper(); side=req.side.lower(); qty=float(req.qty); assets=await fetch_market(); found=next((a for a in assets if a["symbol"]==symbol),None)
    if not found: return {"ok":False,"message":"Ativo não disponível no ticker."}
    price=float(req.price or found["price"]); cost=qty*price
    if side=="buy":
        if paper["cash"]<cost: return {"ok":False,"message":"Saldo PAPER insuficiente."}
        paper["cash"]-=cost; existing=next((p for p in paper["positions"] if p["symbol"]==symbol),None)
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

# ---- Broker connection: Binance READ-ONLY session test ----
class BinanceConnectRequest(BaseModel):
    api_key: str = Field(min_length=8, max_length=300)
    api_secret: str = Field(min_length=8, max_length=300)


def binance_signature(secret: str, query: str) -> str:
    return hmac.new(secret.encode(), query.encode(), hashlib.sha256).hexdigest()

@app.post("/api/broker/binance/connect")
async def connect_binance(req: BinanceConnectRequest):
    # Credentials are used only for this request and are NOT persisted in the application.
    timestamp=int(time.time()*1000); recv_window=5000
    query=f"recvWindow={recv_window}&timestamp={timestamp}"
    signature=binance_signature(req.api_secret, query)
    headers={"X-MBX-APIKEY":req.api_key}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r=await client.get("https://api.binance.com/api/v3/account",params={"recvWindow":recv_window,"timestamp":timestamp,"signature":signature},headers=headers)
        if r.status_code != 200:
            return {"ok":False,"connected":False,"message":"A Binance rejeitou as credenciais ou a chave não tem permissão de leitura.","status_code":r.status_code}
        data=r.json(); balances=[]
        for b in data.get("balances",[]):
            free=float(b.get("free",0)); locked=float(b.get("locked",0))
            if free or locked: balances.append({"asset":b["asset"],"free":free,"locked":locked})
        log("Manager","Conta Binance validada em READ ONLY.","broker")
        return {"ok":True,"connected":True,"broker":"Binance","account_type":data.get("accountType"),"can_trade":bool(data.get("canTrade")),"balances":balances[:80],"message":"Conta validada. As credenciais não foram guardadas."}
    except Exception as exc:
        return {"ok":False,"connected":False,"message":f"Falha de ligação: {type(exc).__name__}."}

@app.get("/api/broker/status")
def broker_status():
    return {"connected":False,"broker":None,"mode":"READ_ONLY SESSION","message":"Nenhuma sessão de corretora ativa neste pedido. Ligue uma conta para validar saldo e permissões."}
