import os, json, time, hmac, hashlib, base64
from urllib.request import urlopen, Request
from urllib.parse import urlparse

USERNAME = os.environ.get("OWNER_USERNAME", "owner")
PASSWORD = os.environ.get("OWNER_PASSWORD", "ChangeMe-2026!")
SESSION_SECRET = os.environ.get("SESSION_SECRET", "change-this-secret-in-vercel")

EVENTS = [
    {"time": "online", "agent": "Manager", "text": " verificando necessidades de capacidades."},
    {"time": "online", "agent": "Market Scanner", "text": " a recolher dados públicos de mercado."},
    {"time": "online", "agent": "Risk", "text": " a validar sinais recebidos."},
    {"time": "online", "agent": "Executor", "text": " bloqueado por Governance."},
]

def _token():
    ts = str(int(time.time() // 3600))
    sig = hmac.new(SESSION_SECRET.encode(), ts.encode(), hashlib.sha256).hexdigest()
    return ts + "." + sig

def _valid_cookie(headers):
    raw = headers.get("cookie", "")
    token = ""
    for part in raw.split(";"):
        if part.strip().startswith("session="):
            token = part.strip().split("=", 1)[1]
    if "." not in token:
        return False
    ts, sig = token.split(".", 1)
    try:
        if abs(int(time.time() // 3600) - int(ts)) > 24:
            return False
    except Exception:
        return False
    expected = hmac.new(SESSION_SECRET.encode(), ts.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)

def _json_response(start_response, status, data, headers=None):
    body = json.dumps(data).encode()
    hs = [("Content-Type","application/json"),("Cache-Control","no-store")]
    if headers: hs.extend(headers)
    start_response(status, hs)
    return [body]

def _read_json(environ):
    try:
        n = int(environ.get("CONTENT_LENGTH") or 0)
        return json.loads(environ["wsgi.input"].read(n) or b"{}")
    except Exception:
        return {}

def app(environ, start_response):
    path = urlparse(environ.get("PATH_INFO","/")).path
    method = environ.get("REQUEST_METHOD","GET")

    if path == "/api/login" and method == "POST":
        data = _read_json(environ)
        if data.get("username") == USERNAME and data.get("password") == PASSWORD:
            return _json_response(start_response,"200 OK",{"ok":True},[
                ("Set-Cookie",f"session={_token()}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=86400")
            ])
        return _json_response(start_response,"401 Unauthorized",{"ok":False,"error":"invalid_credentials"})

    if path == "/api/logout":
        return _json_response(start_response,"200 OK",{"ok":True},[
            ("Set-Cookie","session=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0")
        ])

    if path in ("/api/state","/api/market"):
        if not _valid_cookie(environ.get("HTTP_COOKIE","")):
            return _json_response(start_response,"401 Unauthorized",{"error":"unauthorized"})
        if path == "/api/state":
            return _json_response(start_response,"200 OK",{"events":EVENTS})
        return _market(start_response)

    if path == "/health":
        return _json_response(start_response,"200 OK",{"status":"online","service":"crypto-ai-multi-agent","mode":"read-only"})

    return _json_response(start_response,"404 Not Found",{"detail":"Not Found"})

def _market(start_response):
    symbols = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT","BNBUSDT","ADAUSDT"]
    try:
        qs = "&".join(f"symbol={s}" for s in symbols)
        req = Request("https://api.binance.com/api/v3/ticker/24hr?" + qs, headers={"User-Agent":"crypto-ai-multi-agent/1.0"})
        with urlopen(req, timeout=8) as r:
            raw = json.loads(r.read().decode())
        data = [{"symbol":x["symbol"],"price":x["lastPrice"],"change":x["priceChangePercent"]} for x in raw]
        return _json_response(start_response,"200 OK",{"data":data,"source":"Binance public market data"})
    except Exception as e:
        return _json_response(start_response,"200 OK",{"data":[],"source":"unavailable","error":str(e)})

# Vercel's Python runtime can use a WSGI callable named app.
