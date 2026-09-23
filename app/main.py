
import os, time, hmac, hashlib, secrets
from collections import defaultdict, deque
from typing import Optional
import httpx
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Crypto AI Multi-Agent V1.1")

ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:8000")
LIVE_TRADING = os.getenv("LIVE_TRADING", "false").lower() == "true"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["Content-Type","X-CSRF-Token"],
)

RATE = defaultdict(deque)
SESSIONS = {}
AUDIT = deque(maxlen=500)
AGENTS = [
    {"id":"manager","name":"Manager","status":"working","role":"Orquestrador"},
    {"id":"scanner","name":"Market Scanner","status":"working","role":"Pesquisa de Mercado"},
    {"id":"risk","name":"Risk Manager","status":"working","role":"Gestão de Risco"},
    {"id":"executor","name":"Executor","status":"blocked","role":"Execução"},
    {"id":"cio","name":"CIO","status":"vacancy","role":"Estratégia"},
    {"id":"fundamental","name":"Fundamentalista","status":"vacancy","role":"Fundamentos"},
    {"id":"sentiment","name":"Sentimento","status":"vacancy","role":"Sentimento"},
    {"id":"liquidity","name":"Liquidez","status":"vacancy","role":"Liquidez"},
    {"id":"compliance","name":"Compliance","status":"vacancy","role":"Conformidade"},
    {"id":"arbitrage","name":"Arbitragem","status":"vacancy","role":"Arbitragem"},
]
CSRF = {}

def env(name, default=""):
    return os.getenv(name, default)

def verify_password(password: str) -> bool:
    stored = env("OWNER_PASSWORD_HASH")
    try:
        alg, iters, salt_hex, digest_hex = stored.split("$")
        if alg != "pbkdf2_sha256":
            return False
        got = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(iters))
        return hmac.compare_digest(got.hex(), digest_hex)
    except Exception:
        return False

def rate_limit(key: str, limit=30, window=60):
    now = time.time()
    q = RATE[key]
    while q and now - q[0] > window:
        q.popleft()
    if len(q) >= limit:
        raise HTTPException(429, "Too many requests")
    q.append(now)

def audit(event, request: Request, detail=""):
    AUDIT.append({
        "ts": int(time.time()),
        "event": event,
        "ip": request.client.host if request.client else "unknown",
        "detail": detail[:500]
    })

def issue_session(email: str):
    sid = secrets.token_urlsafe(32)
    csrf = secrets.token_urlsafe(32)
    SESSIONS[sid] = {"email": email, "created": time.time(), "expires": time.time()+8*3600, "revoked": False, "csrf": csrf}
    return sid, csrf

def current_session(request: Request):
    sid = request.cookies.get("owner_session")
    if not sid or sid not in SESSIONS:
        raise HTTPException(401, "Authentication required")
    s = SESSIONS[sid]
    if s["revoked"] or s["expires"] < time.time():
        SESSIONS.pop(sid, None)
        raise HTTPException(401, "Session expired")
    return sid, s

def owner(request: Request):
    sid, s = current_session(request)
    return sid, s

def protected_post(request: Request):
    sid, s = owner(request)
    supplied = request.headers.get("X-CSRF-Token","")
    if not supplied or not hmac.compare_digest(supplied, s["csrf"]):
        audit("csrf_rejected", request)
        raise HTTPException(403, "CSRF validation failed")
    return sid, s

class Login(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=200)

class Action(BaseModel):
    agent_id: str
    action: str

class Mission(BaseModel):
    objective: str = Field(min_length=3, max_length=1000)

class Chat(BaseModel):
    message: str = Field(min_length=1, max_length=4000)

class BrokerConnect(BaseModel):
    api_key: str = Field(min_length=8, max_length=256)
    api_secret: str = Field(min_length=8, max_length=256)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    return response

@app.get("/health")
def health():
    return {"ok": True, "live_trading": False, "version":"1.1"}

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """<!doctype html><html><head><meta charset=utf-8><title>Owner Login</title>
<style>body{background:#0b1020;color:#fff;font-family:Arial;display:grid;place-items:center;height:100vh}
.card{width:360px;background:#141b30;padding:28px;border-radius:16px}input,button{width:100%;padding:12px;margin:8px 0;box-sizing:border-box}
button{background:#37d67a;border:0;font-weight:700;cursor:pointer}</style></head>
<body><div class=card><h2>Crypto AI Office</h2><p>Owner Access</p>
<form id=f><input id=e type=email placeholder="Email" required><input id=p type=password placeholder="Password" required>
<button>Entrar</button></form><pre id=o></pre></div>
<script>
f.onsubmit=async(e)=>{e.preventDefault();let r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:e.value,password:p.value})});
o.textContent=r.ok?'Login efetuado. Abra /dashboard':'Login inválido';if(r.ok)location='/dashboard'}
</script></body></html>"""

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        _, s = current_session(request)
    except HTTPException:
        return HTMLResponse("<script>location='/login'</script>")
    return """<!doctype html><html><head><meta charset=utf-8><title>Trading Office</title>
<style>
body{margin:0;background:#07111f;color:#eaf2ff;font-family:Arial}
header{padding:14px 22px;border-bottom:1px solid #20304a;display:flex;justify-content:space-between}
main{display:grid;grid-template-columns:1fr 360px;gap:16px;padding:16px}
.office{background:#101c2e;border:1px solid #2b4162;border-radius:18px;padding:18px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.desk{background:#16253a;border:1px solid #355273;border-radius:12px;padding:15px;min-height:100px}
.working{box-shadow:inset 0 0 0 1px #2ed67a}.blocked{box-shadow:inset 0 0 0 1px #e6a93a}
.side{display:grid;gap:16px}.panel{background:#101c2e;border:1px solid #2b4162;border-radius:18px;padding:16px}
button{background:#2ed67a;border:0;padding:10px 14px;border-radius:8px;font-weight:700;cursor:pointer}
small{color:#8fa6c4}
</style></head><body><header><b>CRYPTO AI TRADING OFFICE V1.1</b><button onclick="logout()">Sair</button></header>
<main><section class=office><h2>Escritório</h2><div id=agents class=grid></div></section>
<section class=side><div class=panel><h3>Segurança</h3><p>Owner autenticado</p><p>LIVE TRADING: <b>DESATIVADO</b></p></div>
<div class=panel><h3>Auditoria</h3><pre id=logs></pre></div></section></main>
<script>
const esc=s=>String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
async function load(){let r=await fetch('/api/office');if(r.status===401)return location='/login';let d=await r.json();
agents.innerHTML=d.agents.map(a=>`<div class="desk ${esc(a.status)}"><b>${esc(a.name)}</b><br><small>${esc(a.role)}</small><p>${esc(a.status)}</p></div>`).join('');
let l=await fetch('/api/audit');logs.textContent=JSON.stringify((await l.json()).items,null,2)}
async function logout(){await fetch('/api/logout',{method:'POST',headers:{'X-CSRF-Token':window.csrf||''}});location='/login'} load();
</script></body></html>"""

@app.post("/api/login")
def login(data: Login, request: Request, response: Response):
    rate_limit("login:"+ (request.client.host if request.client else "unknown"), 8, 300)
    if not hmac.compare_digest(data.email.lower(), env("OWNER_EMAIL").lower()) or not verify_password(data.password):
        audit("login_failed", request)
        raise HTTPException(401, "Invalid credentials")
    sid, csrf = issue_session(data.email.lower())
    response.set_cookie("owner_session", sid, httponly=True, secure=request.url.scheme=="https",
                        samesite="strict", max_age=8*3600, path="/")
    audit("login_success", request)
    return {"ok":True,"csrf":csrf}

@app.post("/api/logout")
def logout(request: Request, response: Response):
    sid, s = current_session(request)
    token = request.headers.get("X-CSRF-Token","")
    if not hmac.compare_digest(token, s["csrf"]):
        raise HTTPException(403, "CSRF validation failed")
    SESSIONS[sid]["revoked"]=True
    response.delete_cookie("owner_session", path="/")
    audit("logout", request)
    return {"ok":True}

@app.get("/api/session")
def session(request: Request):
    _, s = owner(request)
    return {"email":s["email"],"expires":int(s["expires"]),"csrf":s["csrf"]}

@app.get("/api/office")
def office(request: Request):
    owner(request)
    return {"agents":AGENTS,"live_trading":False}

@app.post("/api/agents/action")
def agent_action(data: Action, request: Request):
    sid,s=protected_post(request); rate_limit("action:"+s["email"],60,60)
    if data.action not in {"start","pause","block"}:
        raise HTTPException(400,"Invalid action")
    for a in AGENTS:
        if a["id"]==data.agent_id:
            a["status"]={"start":"working","pause":"paused","block":"blocked"}[data.action]
            audit("agent_action",request,f"{data.agent_id}:{data.action}")
            return {"ok":True,"agent":a}
    raise HTTPException(404,"Agent not found")

@app.post("/api/missions")
def mission(data: Mission, request: Request):
    sid,s=protected_post(request); rate_limit("mission:"+s["email"],20,60)
    audit("mission_created",request,data.objective)
    return {"ok":True,"status":"queued","objective":data.objective}

@app.post("/api/chat")
async def chat(data: Chat, request: Request):
    sid,s=protected_post(request); rate_limit("chat:"+s["email"],20,60)
    key=env("OPENAI_API_KEY")
    if not key:
        return {"ok":True,"mode":"local","reply":"OpenAI ainda não está configurada. O Manager recebeu a mensagem em modo local."}
    model=env("OPENAI_MODEL","gpt-5")
    headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"}
    payload={"model":model,"input":[{"role":"system","content":"You are the Manager of a controlled crypto investment office. Do not execute trades. Explain risks and require Owner approval for privileged actions."},{"role":"user","content":data.message}]}
    async with httpx.AsyncClient(timeout=30) as client:
        r=await client.post("https://api.openai.com/v1/responses",headers=headers,json=payload)
    if r.status_code>=400:
        audit("openai_error",request,str(r.status_code))
        raise HTTPException(502,"AI provider error")
    j=r.json()
    audit("chat",request,"OpenAI request")
    return {"ok":True,"mode":"openai","reply":j.get("output_text","")}

@app.post("/api/broker/binance/read-only")
async def binance_read_only(data: BrokerConnect, request: Request):
    sid,s=protected_post(request); rate_limit("binance:"+s["email"],10,300)
    # Never persist the supplied secret.
    import urllib.parse
    ts=int(time.time()*1000)
    query=f"timestamp={ts}"
    signature=hmac.new(data.api_secret.encode(),query.encode(),hashlib.sha256).hexdigest()
    url="https://api.binance.com/api/v3/account?"+query+"&signature="+signature
    headers={"X-MBX-APIKEY":data.api_key}
    async with httpx.AsyncClient(timeout=15) as client:
        r=await client.get(url,headers=headers)
    if r.status_code>=400:
        audit("binance_read_only_failed",request,"provider rejected credentials")
        raise HTTPException(400,"Binance rejected the credentials or permissions")
    j=r.json()
    if j.get("canTrade"):
        audit("binance_permission_warning",request,"API key can trade; connection remains READ ONLY")
    audit("binance_read_only_success",request,"credentials not persisted")
    balances=[b for b in j.get("balances",[]) if float(b.get("free","0")) or float(b.get("locked","0"))]
    return {"ok":True,"mode":"READ_ONLY","can_trade":bool(j.get("canTrade")),"can_withdraw":bool(j.get("canWithdraw")),"balances":balances}

@app.get("/api/audit")
def audit_view(request: Request):
    owner(request)
    return {"items":list(AUDIT)[-100:]}

@app.post("/api/live/order")
def live_order_blocked(request: Request):
    protected_post(request)
    raise HTTPException(403,"LIVE trading is disabled in V1.1")

@app.get("/")
def root():
    return HTMLResponse("<script>location='/login'</script>")
