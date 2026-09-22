# Architecture V0.1

```text
                         OWNER
                           |
                 approve / reject
                           |
                           v
                    GOVERNANCE LAYER
                           |
                           v
+------------------------------------------------+
|              MANAGER — AGENT 01                |
|     coordinates, evaluates, requests agents   |
+------------------------+-----------------------+
                         |
              existing agents / requests
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
     Scanner           Risk           Executor
     research         controls        DISABLED
```

## Core rule

The Manager is not the Owner.

The Manager may say:

> "I need a Pattern Agent because the current agents cannot perform structured technical-pattern analysis."

It must produce a justification report. The request is stored as `PENDING`.

The Owner decides.

Only an `APPROVED` request can later become an authorized agent creation operation.
