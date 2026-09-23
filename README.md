# Crypto AI Multi-Agent Trading Office — V0.9.0

Versão focada no **escritório visual**, controlo do Owner, dados de mercado, integração com IA e conexão segura em sessão com uma conta Binance em **READ ONLY**.

## O que funciona
- Escritório pixel-art como painel central, com 10 postos.
- 4 agentes atuais + 6 vagas estratégicas.
- Manager, Market Scanner e Risk começam ativos.
- Executor pode ser autorizado para **PAPER** pelo Owner.
- Cotações públicas por Binance 24h, com fallback CoinGecko.
- Portfólio PAPER e simulador de ordens.
- Missões Manager → Scanner → Risk → Executor PAPER.
- Chat / Chefe com fallback local.
- Se `OPENAI_API_KEY` estiver configurada, o Chat usa a **OpenAI Responses API** no backend; a chave não é enviada para o browser.
- Página Corretora com ligação **Binance READ ONLY**: API Key + Secret são usados apenas para validar a conta no pedido e não são persistidos nesta versão.
- Dashboard com atividade, patrimônio, estado da equipe e mercado.

## Segurança nesta versão
Esta versão **não envia ordens LIVE**. A conexão Binance é somente de leitura e não guarda a API Secret.

Para conectar uma conta Binance, crie uma API Key com leitura e **sem permissões de levantamento**. Nunca coloque a chave em GitHub.

Para execução LIVE real seria necessário implementar uma camada adicional de custódia de segredos, autenticação do Owner, limites de risco, auditoria e confirmação explícita de cada operação. Não está habilitada nesta versão.

## OpenAI no Vercel
No projeto Vercel, em Settings → Environment Variables, adicione:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5
```

Depois faça um novo deploy. Variáveis de ambiente são disponibilizadas ao backend e não devem ser colocadas no código do frontend.

## Vercel
O projeto mantém FastAPI no backend e arquivos estáticos no mesmo deployment.

## Executar localmente
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Abra `http://localhost:8000`.
