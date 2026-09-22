# Crypto AI Multi-Agent Trading Office — V0.7.0

Rebuild do Command Center com interface de trading office, ticker de mercado, escritório 32-bit, equipe, missões, relatórios, chat com Manager, governance e área preparada para corretora.

## Estado desta versão
- Dados públicos de mercado: Binance 24h ticker via backend.
- Fallback local caso a API de mercado falhe.
- Corretora: não conectada.
- Trading LIVE: bloqueado.
- Missões: teste de fluxo Manager → Scanner → Risk → Executor.
- Executor: bloqueado por Governance.

## Executar localmente
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
Abra `http://localhost:8000`.

## Vercel
O projeto inclui `vercel.json` e usa `app/main.py` como função Python. Faça push para GitHub e importe o repositório na Vercel.

## API
- `/health`
- `/api/market`
- `/api/office`
- `/api/portfolio`
- `/api/reports`
- `POST /api/chat`
- `POST /api/missions`

## Segurança
Nunca coloque chaves da corretora no JavaScript. A futura integração deve guardar credenciais apenas no backend/variáveis de ambiente, começar em READ ONLY e usar permissões mínimas.
