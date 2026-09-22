from fastapi import FastAPI
from app.api import agents, governance, dashboard, office

app = FastAPI(
    title="Crypto AI Multi-Agent",
    version="0.3.0",
    description="Private multi-agent trading office with Owner controls and team governance.",
)

app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(governance.router, prefix="/governance", tags=["governance"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(office.router, prefix="/office", tags=["office"])

@app.get("/")
def root():
    return {
        "name": "Crypto AI Multi-Agent",
        "status": "online",
        "version": "0.3.0",
        "message": "Agent Office is online.",
        "dashboard": "/dashboard",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.3.0"}
