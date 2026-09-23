import os
os.environ.setdefault("OWNER_EMAIL", "owner@example.com")
os.environ.setdefault("OWNER_PASSWORD_HASH", "pbkdf2_sha256$310000$ZHVtbXlzYWx0MTIzNDU2$Jb8b6Z2u8H6wQ2z1YQe4zYj0qgYl9rZ0Gx5lF8yX9c8=")
os.environ.setdefault("SESSION_SECRET", "test-secret-please-change-in-production")

from fastapi.testclient import TestClient
from app.main import app, password_hash

client = TestClient(app)

# Replace env hash with a deterministic runtime hash for tests.
os.environ["OWNER_PASSWORD_HASH"] = password_hash("TestPassword!123")


def login():
    r = client.post("/api/auth/login", json={"email":"owner@example.com","password":"TestPassword!123"})
    assert r.status_code == 200
    return r.json()["csrf"]


def test_public_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["version"] == "1.0.0"


def test_protected_endpoint_requires_auth():
    r = client.get("/api/office")
    assert r.status_code == 401


def test_login_and_csrf_protection():
    csrf = login()
    assert client.get("/api/office").status_code == 200
    bad = client.post("/api/agents/action", json={"agent_id":"agent-01","action":"pause"})
    assert bad.status_code == 403
    good = client.post("/api/agents/action", headers={"X-CSRF-Token":csrf}, json={"agent_id":"agent-01","action":"pause"})
    assert good.status_code == 200
    assert good.json()["ok"] is True


def test_binance_requires_auth_and_csrf():
    client.post("/api/auth/logout", headers={"X-CSRF-Token":client.cookies.get("ca_csrf", "")})
    r = client.post("/api/broker/binance/connect", json={"api_key":"abcdefgh","api_secret":"abcdefgh"})
    assert r.status_code == 401


def test_paper_order_requires_csrf():
    csrf = login()
    r = client.post("/api/paper/order", json={"symbol":"BTC","side":"buy","qty":0.0001})
    assert r.status_code == 403
    r = client.post("/api/paper/order", headers={"X-CSRF-Token":csrf}, json={"symbol":"BTC","side":"buy","qty":0.0001})
    assert r.status_code == 200
    assert r.json()["mode"] == "PAPER"
