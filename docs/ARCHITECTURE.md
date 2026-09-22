# Arquitetura V0.7

```text
MARKET DATA -> FastAPI -> Dashboard + Market Scanner
                         |
OWNER -> Manager -> agentes -> Risk -> Governance -> Executor
                         |
                    Audit/Reports
                         |
                    Broker Adapter
```

A UI não deve falar diretamente com a corretora. O backend será o único ponto de integração.
