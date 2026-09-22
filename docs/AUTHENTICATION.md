# Authentication / Authorization — V0.1

V0.1 deliberately keeps the authentication layer minimal because this release is a governance/architecture prototype.

## Current identity model

The Owner is represented by:

```text
OWNER_ID=owner-001
```

Owner-only approval endpoints receive `owner_id` and compare it with the configured Owner ID.

Example:

```python
if owner_id != governance.owner_id:
    raise HTTPException(status_code=403, detail="Only Owner can approve.")
```

## Important limitation

This is **not production authentication**. `owner_id` is an identifier, not a cryptographic credential.

`JWT_SECRET` exists in `.env.example` for the next authentication layer, but V0.1 does not yet issue or validate JWTs.

Production version should use:
- password hashing;
- short-lived access tokens;
- refresh-token rotation;
- secure HTTP-only cookies or Authorization headers;
- role/permission claims;
- server-side audit logging;
- secret storage outside Git;
- TLS.

No exchange API keys belong in this repository.
