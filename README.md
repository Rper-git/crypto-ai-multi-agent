# Crypto AI Multi-Agent — V0.6.0

AI Financial Office with a Command Center, Owner governance, team roles, broker configuration, reports, Chief chat, and a safe end-to-end simulation workflow.

## What works in V0.6
- FastAPI API and dashboard on Vercel.
- Four current agents with missions and skills.
- Owner-only agent activation/deactivation.
- Team vacancies with financial-market skills.
- Broker configuration in PAPER/READ_ONLY/LIVE labels; **no real secrets are stored**.
- Reports and Chief/Advisor conversation.
- **End-to-end test mission**: Manager → Market Scanner → Risk → Manager.
- Simulation never submits a real order and explicitly returns `NO_LIVE_TRADE`.

## Test
Open `/dashboard`, select **Missões**, and run a cycle with a small test capital value.

API:
- `POST /office/test-cycle`
- `GET /office/missions`
- `GET /dashboard/state`
- `GET /docs`

## Safety boundary
This release is an architecture and simulation test. It is not connected to a broker and does not execute real trades. Real broker execution requires a dedicated connector, secure secret management, audit trail, risk limits, paper testing and explicit Owner controls.
