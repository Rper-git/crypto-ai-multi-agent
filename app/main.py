from fastapi import FastAPI
from app.api import agents, governance, dashboard, office, workflow
app=FastAPI(title='Crypto AI Multi-Agent',version='0.6.0',description='Private AI financial office with broker configuration, reports, team management and Owner governance.')
app.include_router(agents.router,prefix='/agents',tags=['agents']); app.include_router(governance.router,prefix='/governance',tags=['governance']); app.include_router(dashboard.router,prefix='/dashboard',tags=['dashboard']); app.include_router(office.router,prefix='/office',tags=['office']); app.include_router(workflow.router,prefix='/office',tags=['workflow'])
@app.get('/')
def root(): return {'name':'Crypto AI Multi-Agent','status':'online','version':'0.6.0','dashboard':'/dashboard','docs':'/docs','health':'/health'}
@app.get('/health')
def health(): return {'status':'ok','version':'0.6.0'}
