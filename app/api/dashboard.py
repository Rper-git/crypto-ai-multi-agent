from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.registry import registry
from app.services.governance import governance

router = APIRouter()


def _activity_for(agent_id: str, cycle: int, status: str) -> str:
    if status == "DISABLED":
        return "Desativado pelo Owner"
    if agent_id == "agent-04":
        return "Executor autorizado e disponível para o próximo ciclo"
    activities = {
        "agent-01": ["Orquestrando o ciclo de análise", "Avaliando tarefas da equipa", "Verificando lacunas de capacidade", "Consolidando relatório do escritório"],
        "agent-02": ["A procurar sinais de mercado", "A comparar pares e timeframes", "A recolher dados de mercado", "A preparar observações para o Risk"],
        "agent-03": ["A avaliar risco das oportunidades", "A verificar exposição e limites", "A validar sinais recebidos", "A preparar parecer de risco"],
    }
    values = activities.get(agent_id, ["Aguardando tarefa"])
    return values[cycle % len(values)]


def dashboard_state():
    now = datetime.now(timezone.utc)
    cycle = int(now.timestamp() // 4)
    agents = []
    for item in registry.list_agents():
        status = item["status"]
        if status == "DISABLED":
            ui_status = "LOCKED"
        elif cycle % 7 == 0 and item["id"] == "agent-03":
            ui_status = "IDLE"
        else:
            ui_status = "WORKING"
        agents.append({**item, "ui_status": ui_status, "activity": _activity_for(item["id"], cycle, status), "last_tick": now.isoformat()})

    events = registry.events()
    return {
        "office": {
            "total_agents": len(agents),
            "working": sum(a["ui_status"] == "WORKING" for a in agents),
            "idle": sum(a["ui_status"] == "IDLE" for a in agents),
            "locked": sum(a["ui_status"] == "LOCKED" for a in agents),
        },
        "agents": agents,
        "pending_requests": len([r for r in governance.list_requests() if r["status"] == "PENDING"]),
        "events": events,
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
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Crypto AI Multi-Agent — Agent Office</title>
<style>
:root{--bg:#070a10;--panel:#0e141d;--panel2:#111a26;--line:#263244;--text:#edf3fa;--muted:#8e9bae;--accent:#61dafb;--green:#45d483;--amber:#f5bd55;--red:#ff6b6b;--blue:#6ea8fe}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 50% -10%,#17253a 0,#070a10 42%);color:var(--text);font:14px/1.45 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}.shell{max-width:1540px;margin:0 auto;padding:24px}.top{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin-bottom:20px}.eyebrow{color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}.title{font-size:30px;font-weight:850;margin:5px 0}.subtitle{color:var(--muted)}.live{display:flex;align-items:center;gap:8px;background:#0d1b17;border:1px solid #1f4c3a;border-radius:999px;padding:9px 13px;color:#b8f5d3;font-weight:700}.dot{width:8px;height:8px;border-radius:50%;background:var(--green)}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}.metric{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:14px;padding:16px}.label{color:var(--muted);font-size:11px}.value{font-size:28px;font-weight:850;margin-top:4px}.hint{font-size:11px;color:var(--muted);margin-top:4px}.layout{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(330px,.85fr);gap:16px}.panel{background:rgba(14,20,29,.95);border:1px solid var(--line);border-radius:16px;overflow:hidden}.panel-head{padding:15px 18px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}.panel-title{font-weight:800}.panel-note{font-size:12px;color:var(--muted)}.office{padding:16px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}.desk{position:relative;min-height:205px;border:1px solid #2a394d;border-radius:14px;background:linear-gradient(145deg,#121c29,#0b1119);padding:15px;overflow:hidden}.desk:after{content:"";position:absolute;inset:auto 0 0 0;height:3px;background:var(--line)}.desk.working:after{background:var(--green)}.desk.idle:after{background:var(--amber)}.desk.locked:after{background:var(--red)}.desk-top{display:flex;justify-content:space-between;gap:10px}.robot{width:58px;height:58px;border:1px solid #3a4a61;border-radius:15px;display:grid;place-items:center;background:#0a1018;font-size:27px;margin-bottom:10px}.agent-name{font-size:17px;font-weight:800}.role{color:var(--muted);font-size:12px}.badge{font-size:10px;font-weight:800;letter-spacing:.07em;border-radius:999px;padding:5px 8px;height:max-content}.badge.working{background:#103022;color:#8ef0b7}.badge.idle{background:#352a12;color:#ffd57d}.badge.locked{background:#35181b;color:#ff9a9a}.activity{margin-top:9px;color:#c7d2df;font-size:12px;min-height:35px}.meter{margin-top:10px;height:5px;background:#1a2432;border-radius:99px;overflow:hidden}.meter span{display:block;height:100%;background:var(--accent);width:78%;border-radius:99px}.working .meter span{animation:pulse 1.8s ease-in-out infinite}.locked .meter span{width:14%;background:var(--red)}.idle .meter span{width:38%;background:var(--amber)}@keyframes pulse{50%{width:92%;opacity:.6}}.desk-actions{display:flex;gap:7px;margin-top:11px;flex-wrap:wrap}.btn{border:1px solid #304156;background:#121b27;color:#d9e4f0;border-radius:9px;padding:8px 10px;font-weight:750;font-size:11px;cursor:pointer}.btn:hover{border-color:#5b7592}.btn.primary{border-color:#2e8060;background:#123021;color:#a9f3c8}.btn.danger{border-color:#7c3539;background:#2a1518;color:#ffb0b0}.side{display:flex;flex-direction:column;gap:16px}.feed{padding:8px 18px 18px}.event{padding:12px 0;border-bottom:1px solid #1d2735}.event:last-child{border:0}.event-head{display:flex;justify-content:space-between;gap:10px}.event-agent{font-weight:750}.event-time{font-size:11px;color:var(--muted)}.event-text{color:#aebaca;font-size:12px;margin-top:3px}.rule{margin:0 18px 15px;padding:12px;border-radius:12px;background:#111c2a;border:1px solid #26384e;color:#b7c6d7;font-size:12px}.rule strong{color:#fff}.actions{display:flex;gap:8px;flex-wrap:wrap;padding:0 18px 18px}.action{border:1px solid #304156;background:#121b27;color:#d9e4f0;border-radius:10px;padding:9px 11px;text-decoration:none;font-weight:700;font-size:12px}.chat{display:flex;flex-direction:column;height:430px}.chat-log{flex:1;overflow:auto;padding:14px}.msg{max-width:88%;padding:10px 11px;border-radius:12px;margin-bottom:9px;border:1px solid var(--line);font-size:12px}.msg.owner{margin-left:auto;background:#102433;border-color:#25475e}.msg.chief{background:#121a25}.msg .who{font-weight:800;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:3px}.chat-form{border-top:1px solid var(--line);padding:11px;display:flex;gap:8px}.chat-input{flex:1;min-width:0;background:#090f17;border:1px solid #304156;color:var(--text);border-radius:10px;padding:10px;font:inherit;outline:none}.chat-input:focus{border-color:var(--accent)}.chat-title{padding:13px 18px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between}.modal{position:fixed;inset:0;background:rgba(0,0,0,.72);display:none;align-items:center;justify-content:center;padding:18px;z-index:10}.modal.open{display:flex}.modal-card{width:min(460px,100%);background:#0e141d;border:1px solid #34465d;border-radius:16px;padding:20px;box-shadow:0 20px 70px rgba(0,0,0,.5)}.modal-card h3{margin:0 0 7px}.modal-card p{color:var(--muted);font-size:12px}.modal-input{width:100%;padding:11px;background:#080d14;border:1px solid #304156;border-radius:10px;color:#fff;font:inherit}.modal-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:15px}.notice{margin-top:10px;color:#ffb0b0;font-size:12px;min-height:17px}.foot{color:#6f7d8e;font-size:11px;padding:0 18px 17px}@media(max-width:1050px){.layout{grid-template-columns:1fr}}@media(max-width:700px){.shell{padding:14px}.top{flex-direction:column}.metrics{grid-template-columns:repeat(2,1fr)}.office{grid-template-columns:1fr}.title{font-size:24px}}
</style></head><body>
<main class="shell">
<header class="top"><div><div class="eyebrow">Private AI Trading Office</div><div class="title">Agent Office</div><div class="subtitle">Sala de trabalho • controlo do Owner • diálogo com o Chefe</div></div><div class="live"><span class="dot"></span> SISTEMA ONLINE</div></header>
<section class="metrics"><div class="metric"><div class="label">ROBÔS NO ESCRITÓRIO</div><div class="value" id="total">—</div><div class="hint">agentes registados</div></div><div class="metric"><div class="label">A TRABALHAR</div><div class="value" id="working">—</div><div class="hint">atividade atual</div></div><div class="metric"><div class="label">EM ESPERA</div><div class="value" id="idle">—</div><div class="hint">sem tarefa neste ciclo</div></div><div class="metric"><div class="label">BLOQUEADOS</div><div class="value" id="locked">—</div><div class="hint">sem autorização</div></div></section>
<div class="layout"><section class="panel"><div class="panel-head"><div><div class="panel-title">Sala de trabalho</div><div class="panel-note">Cada posto representa um agente registado.</div></div><div class="panel-note" id="server">—</div></div><div class="office" id="office"></div><div class="foot">O estado visual é simulado nesta versão. A ligação a modelos, dados de mercado e ferramentas reais será adicionada por etapas.</div></section>
<aside class="side">
<section class="panel"><div class="panel-head"><div class="panel-title">Atividade</div><div class="panel-note">live</div></div><div class="feed" id="feed"></div></section>
<section class="panel"><div class="panel-head"><div><div class="panel-title">Conversa com o Chefe</div><div class="panel-note">Alinhamento do escritório</div></div></div><div class="chat"><div class="chat-log" id="chatLog"></div><form class="chat-form" id="chatForm"><input class="chat-input" id="chatInput" autocomplete="off" placeholder="Pergunte sobre a equipa, ideias, metas..."/><button class="btn primary" type="submit">Enviar</button></form></div></section>
<section class="panel"><div class="panel-head"><div class="panel-title">Governance</div><div class="panel-note">Owner</div></div><div class="rule"><strong>Regra:</strong> o Manager propõe; o Owner decide. O Executor só pode ser ativado pelo Owner.</div><div class="actions"><a class="action" href="/docs">API Docs</a><a class="action" href="/health">Health</a><a class="action" href="/governance/agent-requests">Pedidos</a></div></section>
</aside></div></main>
<div class="modal" id="modal"><div class="modal-card"><h3>Ativar Executor</h3><p>Esta ação é reservada ao Owner. Nesta V0.3, o ID abaixo é um mecanismo de desenvolvimento, não autenticação de produção.</p><input class="modal-input" id="ownerId" value="owner-001"/><div class="notice" id="modalError"></div><div class="modal-actions"><button class="btn" type="button" id="cancel">Cancelar</button><button class="btn primary" type="button" id="confirm">Confirmar ativação</button></div></div></div>
<script>
(function(){const $=s=>document.querySelector(s);const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));const icons={'agent-01':'◈','agent-02':'⌁','agent-03':'△','agent-04':'▣'};let selectedAgent=null;
function addMsg(role,text){const d=document.createElement('div');d.className='msg '+role;d.innerHTML='<div class="who">'+(role==='owner'?'Owner':'Chefe')+'</div><div>'+esc(text)+'</div>';$('#chatLog').appendChild(d);$('#chatLog').scrollTop=$('#chatLog').scrollHeight}
async function loadChat(){try{const r=await fetch('/office/chat',{cache:'no-store'});const d=await r.json();$('#chatLog').innerHTML='';d.messages.forEach(m=>addMsg(m.role,m.message))}catch(e){} }
async function sendChat(text){const r=await fetch('/office/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});if(!r.ok)throw new Error('chat');const d=await r.json();$('#chatLog').innerHTML='';d.messages.forEach(m=>addMsg(m.role,m.message))}
$('#chatForm').addEventListener('submit',async e=>{e.preventDefault();const input=$('#chatInput');const text=input.value.trim();if(!text)return;input.value='';try{await sendChat(text)}catch(err){addMsg('chief','Não consegui registar a conversa neste momento.')}});
function openModal(agent){selectedAgent=agent;$('#modalError').textContent='';$('#modal').classList.add('open');$('#ownerId').focus()}
$('#cancel').addEventListener('click',()=>$('#modal').classList.remove('open'));
$('#confirm').addEventListener('click',async()=>{const owner_id=$('#ownerId').value.trim();if(!owner_id){$('#modalError').textContent='Informe o Owner ID.';return}try{const r=await fetch('/agents/'+selectedAgent+'/activate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({owner_id})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Falha');$('#modal').classList.remove('open');await refresh()}catch(e){$('#modalError').textContent=e.message}});
async function deactivate(id){const owner_id=prompt('Owner ID para desativar este agente:','owner-001');if(!owner_id)return;const r=await fetch('/agents/'+id+'/deactivate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({owner_id})});if(!r.ok){const d=await r.json();alert(d.detail||'Falha');return}refresh()}
async function refresh(){try{const r=await fetch('/dashboard/state',{cache:'no-store'});if(!r.ok)throw new Error();const d=await r.json();$('#total').textContent=d.office.total_agents;$('#working').textContent=d.office.working;$('#idle').textContent=d.office.idle;$('#locked').textContent=d.office.locked;$('#server').textContent=new Date(d.server_time).toLocaleTimeString('pt-PT');
$('#office').innerHTML=d.agents.map(a=>{const c=a.ui_status.toLowerCase();const label={WORKING:'A TRABALHAR',IDLE:'EM ESPERA',LOCKED:'BLOQUEADO'}[a.ui_status];let control='';if(a.id==='agent-04'&&a.status==='DISABLED')control='<button class="btn primary activate" data-id="'+esc(a.id)+'">▶ Colocar a trabalhar</button>';else if(a.status==='ACTIVE'&&a.id!=='agent-01')control='<button class="btn danger deactivate" data-id="'+esc(a.id)+'">■ Parar agente</button>';return '<article class="desk '+c+'"><div class="desk-top"><div><div class="robot">'+(icons[a.id]||'◉')+'</div><div class="agent-name">'+esc(a.name)+'</div><div class="role">'+esc(a.role)+' • '+esc(a.id)+'</div></div><span class="badge '+c+'">'+label+'</span></div><div class="activity">'+esc(a.activity)+'</div><div class="meter"><span></span></div><div class="desk-actions">'+control+'</div></article>'}).join('');
$('#office').querySelectorAll('.activate').forEach(b=>b.addEventListener('click',()=>openModal(b.dataset.id)));$('#office').querySelectorAll('.deactivate').forEach(b=>b.addEventListener('click',()=>deactivate(b.dataset.id)));
const base=d.agents.map(a=>'<div class="event"><div class="event-head"><span class="event-agent">'+esc(a.name)+'</span><span class="event-time">'+new Date(a.last_tick).toLocaleTimeString('pt-PT')+'</span></div><div class="event-text">'+esc(a.activity)+'</div></div>').join('');const extra=(d.events||[]).map(e=>'<div class="event"><div class="event-head"><span class="event-agent">Owner control</span><span class="event-time">'+new Date(e.time).toLocaleTimeString('pt-PT')+'</span></div><div class="event-text">'+esc(e.event)+' • '+esc(e.agent_id)+'</div></div>').join('');$('#feed').innerHTML=extra+base}catch(e){$('#server').textContent='offline'}}
loadChat();refresh();setInterval(refresh,3000);
})();</script></body></html>'''
