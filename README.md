# Crypto AI Multi-Agent V1.1 — Security Hardening

This version hardens the V1.0 foundation before Binance integration.

## Included
- Owner login with PBKDF2 password verification
- Signed, expiring HttpOnly/Secure/SameSite session cookie
- CSRF protection for state-changing requests
- Server-side role checks
- In-memory rate limiting with clear production upgrade path
- XSS-safe rendering helper in frontend
- Audit log with security events
- Session revocation endpoint
- Security headers
- Binance READ ONLY adapter scaffold
- OpenAI server-side adapter scaffold
- PAPER trading only
- LIVE trading hard-disabled

## First login
See `OWNER_LOGIN.txt` generated with this package.

## Environment
Copy `.env.example` to `.env` for local development. Never commit `.env`.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `/login`.

## Important
This is a development/security-hardening release, not a production authorization to trade real money.
Before LIVE trading: move rate limits/session state/audit to durable infrastructure, add 2FA/passkeys, secret vault/KMS, database, broker permission verification, idempotency, approval workflow and independent risk controls.
