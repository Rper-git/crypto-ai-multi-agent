# Crypto AI Multi-Agent — V0.2.0

Sistema inicial de orquestração multi-agente para análise de trading.

## Princípio de governança

O **Manager / Agent 01** coordena o sistema. Ele pode identificar a necessidade de um novo agente, mas **não pode criá-lo sozinho**.

Quando precisar de um novo agente, deve gerar uma solicitação com:
- agente solicitado;
- problema que resolve;
- motivo pelo qual os agentes existentes não são suficientes;
- benefício esperado;
- riscos;
- custo/complexidade;
- permissões necessárias.

A solicitação fica `PENDING` até decisão do Owner.

Somente o Owner pode `APPROVE` ou `REJECT`.

## V0.2.0

Esta versão é uma base estrutural. Não executa ordens reais em corretoras e não contém chaves de API de exchanges.

## Estrutura

- `app/` — API FastAPI
- `app/agents/` — agentes
- `app/services/` — registry, governance e auditoria
- `app/db/` — SQLite
- `tests/` — testes básicos
- `.env.example` — configuração


## Vercel

The project is deployable as a FastAPI application on Vercel. After deployment, verify:

- `/` — service status
- `/health` — health check
- `/docs` — FastAPI interactive documentation

No exchange credentials are required in this version. Real trading execution remains disabled.


## Dashboard

A V0.2.0 inclui o Command Center em `/dashboard`, com a sala visual dos agentes, estados, atividade e Governance.
