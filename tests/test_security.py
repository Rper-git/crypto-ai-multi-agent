
from fastapi.testclient import TestClient
import os
os.environ["OWNER_EMAIL"]="owner@cryptooffice.local"
os.environ["OWNER_PASSWORD_HASH"]="pbkdf2_sha256$310000$00112233445566778899aabbccddeeff$" + __import__("hashlib").pbkdf2_hmac("sha256",b"C0mmander!2026",bytes.fromhex("00112233445566778899aabbccddeeff"),310000).hex()
from app.main import app
c=TestClient(app)
def test_login_and_protected():
    r=c.post("/api/login",json={"email":"owner@cryptooffice.local","password":"C0mmander!2026"})
    assert r.status_code==200
    csrf=r.json()["csrf"]
    assert c.get("/api/office").status_code==200
    assert c.post("/api/agents/action",json={"agent_id":"executor","action":"start"}).status_code==403
    assert c.post("/api/agents/action",json={"agent_id":"executor","action":"start"},headers={"X-CSRF-Token":csrf}).status_code==200
def test_live_blocked():
    c.post("/api/login",json={"email":"owner@cryptooffice.local","password":"C0mmander!2026"})
    s=c.get("/api/session").json()
    r=c.post("/api/live/order",headers={"X-CSRF-Token":s["csrf"]})
    assert r.status_code==403
def test_xss_safe_helper_present():
    html=c.get("/dashboard").text
    assert "const esc=" in html
