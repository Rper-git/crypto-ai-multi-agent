# Agent Office — V0.3.0

O `/dashboard` é o centro de comando visual do escritório.

## Controlo do Owner

O Executor aparece como **BLOQUEADO** enquanto seu status for `DISABLED`. O cartão apresenta **Colocar a trabalhar**, que abre uma confirmação de Owner e chama `POST /agents/{agent_id}/activate`.

Agentes ativos podem ser parados pelo Owner através de `POST /agents/{agent_id}/deactivate`.

> Na V0.3, `owner-001` é apenas uma credencial de desenvolvimento. Ainda não representa autenticação de produção.

## Conversa com o Chefe

A caixa "Conversa com o Chefe" permite ao Owner registrar expectativas, objetivos, ideias e perguntas sobre a equipa. O endpoint `/office/chat` mantém um pequeno histórico em memória e devolve respostas determinísticas.

Na próxima fase, o Advisor poderá receber contexto real do escritório, relatórios do Manager, tarefas, métricas e memória persistente, além de um LLM autorizado.
