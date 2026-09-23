# Crypto AI Multi-Agent Trading Office — V1.0 Security Foundation

V1.0 mantém o escritório pixel-art e o modo PAPER, mas adiciona uma camada de segurança antes da integração financeira.

## O que foi corrigido

- Login exclusivo do Owner.
- Sessão assinada com HMAC e expiração de 8 horas.
- Cookie de sessão `HttpOnly`, `Secure` em produção e `SameSite=Strict`.
- CSRF token obrigatório para operações POST autenticadas.
- Rate limiting para login, chat, missões, ações de agentes, PAPER e conexão Binance.
- Cabeçalhos de segurança: HSTS em produção, `X-Frame-Options`, `nosniff`, `Referrer-Policy`, Permissions Policy e CSP.
- Endpoints financeiros e de controle protegidos por autenticação.
- API Key/Secret da Binance continuam sem persistência na aplicação.
- Nenhuma chave OpenAI é enviada ao browser.
- Validação mais restritiva para ordens PAPER.
- LIVE trading continua desligado.

## Variáveis de ambiente obrigatórias

```text
OWNER_EMAIL=owner@example.com
OWNER_PASSWORD_HASH=<hash PBKDF2>
SESSION_SECRET=<segredo aleatório longo>
```

Gerar o hash da password:

```bash
python tools/generate_password_hash.py
```

Gerar um segredo de sessão forte:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Recomendado na Vercel:

```text
ALLOWED_ORIGIN=https://SEU-PROJETO.vercel.app
```

Opcional para o Manager/IA:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5
```

## Endpoints públicos

- `GET /`
- `GET /health`
- `GET /api/market`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/logout`

Os restantes endpoints operacionais exigem sessão do Owner. Operações POST também exigem CSRF.

## Binance

A V1.0 só faz validação **READ ONLY**. Não guarda API Key/Secret e não envia ordens reais.

Ao criar a API Key da Binance, ative apenas leitura e mantenha withdrawals/saques desativados.

## Limitação importante

A V1.0 ainda usa estado em memória para agentes, logs e PAPER. Isso é adequado para testes de uma única instância, mas não é a persistência definitiva para produção financeira. A próxima etapa deve migrar estado, auditoria e sessões de dados operacionais para armazenamento apropriado e manter as credenciais de corretora em um cofre/secret manager.

## Testes

Execute:

```bash
pytest -q
```
