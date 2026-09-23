# Crypto AI Multi-Agent v2

Versão reconstruída sem framework frontend, para evitar a tela branca causada por falhas de build/runtime.

## Deploy no Vercel

1. Importe este projeto no Vercel.
2. Não selecione Next.js/React. O `vercel.json` já define os runtimes.
3. Em Environment Variables, defina:
   - `OWNER_USERNAME` — utilizador do Owner
   - `OWNER_PASSWORD` — palavra-passe forte
   - `SESSION_SECRET` — segredo longo e aleatório
4. Faça Deploy.

### Credenciais padrão apenas para o primeiro teste
- Utilizador: `owner`
- Palavra-passe: `Owner@2026#`

**Troque imediatamente essas credenciais nas Environment Variables.**

## Segurança
- As chaves da Binance não entram no frontend.
- Este build só usa o endpoint público de mercado da Binance.
- Execução de ordens reais permanece bloqueada.
- A autenticação é feita por cookie HttpOnly assinado no backend.
- Antes de ligar execução real, adicionar armazenamento seguro de segredos e uma camada de aprovação do Owner.

## Estrutura
- `index.html` — dashboard completo
- `api/index.py` — login, sessão, estado e proxy de cotações públicas
- `vercel.json` — roteamento Vercel


## Credenciais de acesso

Utilizador padrão: `owner`
Palavra-passe padrão: `Owner@2026#`

Se já existirem variáveis `OWNER_USERNAME` ou `OWNER_PASSWORD` no Vercel, elas têm prioridade. Para usar estas credenciais padrão, remova essas duas variáveis do projeto no Vercel e faça um novo deploy.

Para produção, recomenda-se definir `OWNER_USERNAME`, `OWNER_PASSWORD` e `SESSION_SECRET` nas Environment Variables do Vercel e não colocar segredos no Git.
