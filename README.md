# Crypto AI Multi-Agent — V0.3.0 Agent Office

Sistema privado de orquestração multi-agente para pesquisa e futura execução de trading.

## O que mudou na V0.3.0

- **Agent Office** em `/dashboard`.
- Botão do Owner para colocar o **Executor** a trabalhar.
- Botões para parar agentes ativos (exceto o Manager).
- Estado do escritório calculado a partir do `AgentRegistry`.
- Feed de eventos de controlo.
- Caixa **Conversa com o Chefe** em `/office/chat` para alinhar objetivos, ideias e desenvolvimento da equipa.
- O Manager continua sem poder aprovar ou ativar novos agentes sozinho.

## Controlo do Executor

Na V0.3, a ativação exige `owner_id=owner-001`. Isto é **apenas um mecanismo de desenvolvimento**; não é autenticação de produção.

A ativação do Executor não liga nenhuma exchange e não executa ordens reais. O Executor continua sendo uma estação autorizável, pronta para uma futura camada de execução com limites e governance.

## Conversa com o Chefe

O chat é determinístico e local nesta versão. Ele não usa um LLM externo. O objetivo é criar a interface e o fluxo de alinhamento; uma próxima versão poderá ligar o Chefe/Advisor a um modelo com memória, ferramentas e contexto real do escritório.

## Rotas

- `/` — estado do serviço
- `/health` — health check
- `/dashboard` — Agent Office
- `/dashboard/state` — estado do escritório
- `/office/chat` — conversa com o Chefe
- `/agents` — agentes
- `/docs` — documentação FastAPI

## Segurança

Não colocar chaves de exchanges ou segredos reais no código. Antes de produção, substituir o `owner_id` de desenvolvimento por autenticação real, autorização por função, armazenamento seguro de segredos, auditoria e limites de execução.
