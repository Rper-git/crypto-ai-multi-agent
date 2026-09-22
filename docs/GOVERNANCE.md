# Agent Governance

## Agent creation lifecycle

```text
Manager detects capability gap
        |
        v
Justification report
        |
        v
PENDING
        |
   +----+----+
   |         |
   v         v
APPROVED   REJECTED
   |
   v
Authorized creation
```

The Manager cannot self-authorize a new agent.

## Required justification

1. Requested agent
2. Problem
3. Why existing agents are insufficient
4. Expected benefit
5. Risks
6. Complexity/cost
7. Required permissions

The Owner's decision is recorded with timestamp and Owner ID.
