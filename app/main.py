from fastapi import FastAPI
from app.api import agents, governance

app = FastAPI(
    title="Crypto AI Multi-Agent",
    version="0.1.1",
    description="Multi-agent trading research/orchestration system with Owner approval governance.",
)

app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(governance.router, prefix="/governance", tags=["governance"])

@app.get("/")
def root():
    return {
        "name": "Crypto AI Multi-Agent",
        "status": "online",
        "version": "0.1.1",
        "message": "API is running on Vercel.",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.1"}
