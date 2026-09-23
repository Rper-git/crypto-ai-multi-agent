# Crypto AI Multi-Agent Trading Office — V0.8.0

Interface reconstruída no estilo **trading office pixel-art**, com Command Center funcional.

## Funcionalidades
- Ticker de mercado via backend (Binance 24h → CoinGecko → fallback).
- Escritório visual pixel-art com postos e estados reais dos agentes.
- Controlo do Owner para trabalhar/pausar/bloquear agentes.
- Executor com autorização separada para PAPER; LIVE permanece bloqueado.
- Dashboard de patrimônio PAPER.
- Simulador de BUY/SELL PAPER usando cotações públicas.
- Missões Manager → Scanner → Risk → Executor PAPER.
- Chat com Manager.
- Relatórios e log de atividade.
- Área de corretora preparada para futura ligação READ ONLY.
- Nenhuma chave privada no frontend.

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
O `vercel.json` usa `app/main.py` como função Python.

## Limites de segurança
Esta versão **não envia ordens reais** e não guarda credenciais de corretora. O simulador PAPER é isolado da corretora.
