from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.services.registry import registry
from app.services.governance import governance

router = APIRouter()


def _activity_for(agent_id: str, cycle: int) -> str:
    activities = {
        "agent-01": [
            "Orquestrando o ciclo de análise",
            "Avaliando tarefas dos agentes",
            "Verificando necessidade de novas capacidades",
            "Consolidando relatório do escritório",
        ],
        "agent-02": [
            "A procurar sinais de mercado",
            "A comparar pares e timeframes",
            "A recolher dados de mercado",
            "A preparar observações para o Risk",
        ],
        "agent-03": [
            "A avaliar risco das oportunidades",
            "A verificar exposição e limites",
            "A validar sinais recebidos",
            "A preparar parecer de risco",
        ],
        "agent-04": [
            "Execução desativada por Governance",
            "Aguardando autorização do Owner",
        ],
    }
    values = activities.get(agent_id, ["Aguardando tarefa"])
    return values[cycle % len(values)]


def dashboard_state():
    now = datetime.now(timezone.utc)
    cycle = int(now.timestamp() // 4)
    agents = []
    for item in registry.list_agents():
        status = item["status"]
        if item["id"] == "agent-04":
            ui_status = "LOCKED"
        elif cycle % 7 == 0 and item["id"] == "agent-03":
            ui_status = "IDLE"
        else:
            ui_status = "WORKING"
        agents.append({
            **item,
            "ui_status": ui_status,
            "activity": _activity_for(item["id"], cycle),
            "last_tick": now.isoformat(),
        })

    return {
        "office": {
            "total_agents": len(agents),
            "working": sum(a["ui_status"] == "WORKING" for a in agents),
            "idle": sum(a["ui_status"] == "IDLE" for a in agents),
            "locked": sum(a["ui_status"] == "LOCKED" for a in agents),
        },
        "agents": agents,
        "pending_requests": len([r for r in governance.list_requests() if r["status"] == "PENDING"]),
        "server_time": now.isoformat(),
    }


@router.get("/state")
def state():
    return dashboard_state()


@router.get("", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD_HTML


DASHBOARD_HTML = r'''<!doctype html>
<html lang="pt-PT">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Crypto AI Multi-Agent — Command Center</title>
  <style>
    :root{--bg:#070a10;--panel:#0e141d;--panel2:#111a26;--line:#263244;--text:#edf3fa;--muted:#8e9bae;--accent:#61dafb;--green:#45d483;--amber:#f5bd55;--red:#ff6b6b;}
    *{box-sizing:border-box} body{margin:0;background:radial-gradient(circle at 50% -10%,#17253a 0,#070a10 42%);color:var(--text);font:14px/1.45 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    .shell{max-width:1500px;margin:0 auto;padding:24px}.top{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin-bottom:22px}.eyebrow{color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}.title{font-size:30px;font-weight:800;margin:5px 0}.subtitle{color:var(--muted)}.live{display:flex;align-items:center;gap:8px;background:#0d1b17;border:1px solid #1f4c3a;border-radius:999px;padding:9px 13px;color:#b8f5d3;font-weight:700}.dot{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green)}
    .metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}.metric{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:14px;padding:17px}.metric .label{color:var(--muted);font-size:12px}.metric .value{font-size:28px;font-weight:800;margin-top:4px}.metric .hint{font-size:11px;color:var(--muted);margin-top:4px}
    .layout{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(300px,.8fr);gap:16px}.panel{background:rgba(14,20,29,.92);border:1px solid var(--line);border-radius:16px;overflow:hidden}.panel-head{padding:16px 18px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}.panel-title{font-weight:800}.panel-note{font-size:12px;color:var(--muted)}
    .office{padding:18px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;background:linear-gradient(180deg,rgba(19,28,40,.75),rgba(8,12,18,.8))}.desk{position:relative;min-height:190px;border:1px solid #2a394d;border-radius:14px;background:linear-gradient(145deg,#121c29,#0b1119);padding:16px;overflow:hidden}.desk:after{content:"";position:absolute;inset:auto 0 0 0;height:3px;background:var(--line)}.desk.working:after{background:var(--green)}.desk.idle:after{background:var(--amber)}.desk.locked:after{background:var(--red)}.robot{width:62px;height:62px;border:1px solid #3a4a61;border-radius:16px;display:grid;place-items:center;background:#0a1018;font-size:29px;margin-bottom:12px}.desk-top{display:flex;justify-content:space-between;gap:10px}.agent-name{font-size:17px;font-weight:800}.role{color:var(--muted);font-size:12px}.badge{font-size:10px;font-weight:800;letter-spacing:.08em;border-radius:999px;padding:5px 8px;height:max-content}.badge.working{background:#103022;color:#8ef0b7}.badge.idle{background:#352a12;color:#ffd57d}.badge.locked{background:#35181b;color:#ff9a9a}.activity{margin-top:10px;color:#c7d2df;font-size:12px;min-height:38px}.meter{margin-top:12px;height:5px;background:#1a2432;border-radius:99px;overflow:hidden}.meter span{display:block;height:100%;background:var(--accent);width:78%;border-radius:99px}.working .meter span{animation:pulse 1.8s ease-in-out infinite}.locked .meter span{width:14%;background:var(--red)}.idle .meter span{width:38%;background:var(--amber)}@keyframes pulse{50%{width:92%;opacity:.6}}
    .side{display:flex;flex-direction:column;gap:16px}.feed{padding:8px 18px 18px}.event{padding:13px 0;border-bottom:1px solid #1d2735}.event:last-child{border-bottom:0}.event-head{display:flex;justify-content:space-between;gap:10px}.event-agent{font-weight:750}.event-time{font-size:11px;color:var(--muted)}.event-text{color:#aebaca;font-size:12px;margin-top:3px}.rule{margin:0 18px 18px;padding:13px;border-radius:12px;background:#111c2a;border:1px solid #26384e;color:#b7c6d7;font-size:12px}.rule strong{color:#fff}.actions{display:flex;gap:8px;flex-wrap:wrap;padding:0 18px 18px}.action{border:1px solid #304156;background:#121b27;color:#d9e4f0;border-radius:10px;padding:9px 11px;text-decoration:none;font-weight:700;font-size:12px}.action:hover{border-color:#4a607a}.foot{color:#6f7d8e;font-size:11px;margin-top:14px}
    @media(max-width:900px){.layout{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.shell{padding:14px}.top{flex-direction:column}.office{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}.title{font-size:24px}}
  </style>
</head>
<body>
<main class="shell">
  <header class="top">
    <div><div class="eyebrow">Private AI Trading Office</div><div class="title">Command Center</div><div class="subtitle">Sala de trabalho dos agentes • supervisão pelo Owner</div></div>
    <div class="live"><span class="dot"></span> SISTEMA ONLINE</div>
  </header>

  <section class="metrics" aria-label="Resumo do escritório">
    <div class="metric"><div class="label">ROBÔS NO ESCRITÓRIO</div><div class="value" id="total">—</div><div class="hint">agentes registados</div></div>
    <div class="metric"><div class="label">A TRABALHAR</div><div class="value" id="working">—</div><div class="hint">atividade atual</div></div>
    <div class="metric"><div class="label">EM ESPERA</div><div class="value" id="idle">—</div><div class="hint">sem tarefa neste ciclo</div></div>
    <div class="metric"><div class="label">BLOQUEADOS</div><div class="value" id="locked">—</div><div class="hint">sem autorização de execução</div></div>
  </section>

  <div class="layout">
    <section class="panel">
      <div class="panel-head"><div><div class="panel-title">Sala de trabalho</div><div class="panel-note">Cada posto representa um agente real registado no sistema.</div></div><div class="panel-note" id="server">—</div></div>
      <div class="office" id="office"></div>
      <div class="foot" style="padding:0 18px 18px">A animação representa o estado operacional do sistema. As atividades só serão reais quando ligarmos cada agente aos seus modelos, dados e ferramentas.</div>
    </section>

    <aside class="side">
      <section class="panel"><div class="panel-head"><div class="panel-title">Atividade</div><div class="panel-note">live</div></div><div class="feed" id="feed"></div></section>
      <section class="panel"><div class="panel-head"><div class="panel-title">Governance</div><div class="panel-note">Owner</div></div><div class="rule"><strong>Regra central:</strong> o Manager pode propor um novo agente, mas não pode aprová-lo nem ativá-lo sozinho.</div><div class="actions"><a class="action" href="/docs">API Docs</a><a class="action" href="/health">Health</a><a class="action" href="/governance/agent-requests">Pedidos</a></div></section>
    </aside>
  </div>
</main>
<script>
(function(){
  const $=s=>document.querySelector(s);
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const icons={'agent-01':'◈','agent-02':'⌁','agent-03':'△','agent-04':'▣'};
  async function refresh(){
    try{
      const r=await fetch('/dashboard/state',{cache:'no-store'}); if(!r.ok) throw new Error('state');
      const d=await r.json();
      $('#total').textContent=d.office.total_agents; $('#working').textContent=d.office.working; $('#idle').textContent=d.office.idle; $('#locked').textContent=d.office.locked;
      $('#server').textContent=new Date(d.server_time).toLocaleTimeString('pt-PT');
      $('#office').innerHTML=d.agents.map(a=>{const c=a.ui_status.toLowerCase(); const label={WORKING:'A TRABALHAR',IDLE:'EM ESPERA',LOCKED:'BLOQUEADO'}[a.ui_status]; return `<article class="desk ${c}"><div class="desk-top"><div><div class="robot">${icons[a.id]||'◉'}</div><div class="agent-name">${esc(a.name)}</div><div class="role">${esc(a.role)} • ${esc(a.id)}</div></div><span class="badge ${c}">${label}</span></div><div class="activity">${esc(a.activity)}</div><div class="meter"><span></span></div></article>`}).join('');
      $('#feed').innerHTML=d.agents.map(a=>`<div class="event"><div class="event-head"><span class="event-agent">${esc(a.name)}</span><span class="event-time">${new Date(a.last_tick).toLocaleTimeString('pt-PT')}</span></div><div class="event-text">${esc(a.activity)}</div></div>`).join('');
    }catch(e){$('#server').textContent='offline';}
  }
  refresh(); setInterval(refresh,3000);
})();
</script>
</body></html>'''
