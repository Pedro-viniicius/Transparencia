#!/usr/bin/env bash
# Gera o .env com segredos aleatórios. Não sobrescreve um .env existente.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -f .env ]]; then echo ".env já existe; nada a fazer."; exit 0; fi
umask 077
hex() { openssl rand -hex "$1"; }
PG=$(hex 16)
cat > .env <<ENV
# Gerado por scripts/gerar-env.sh em $(date -Iseconds). NÃO versionar.
POSTGRES_PASSWORD=$PG

# Chatwoot
SECRET_KEY_BASE=$(hex 64)
FRONTEND_URL=http://chatwoot.localhost:3000
DEFAULT_LOCALE=pt_BR
ENABLE_ACCOUNT_SIGNUP=false
ACTIVE_STORAGE_SERVICE=local
RAILS_LOG_TO_STDOUT=true
LOG_LEVEL=info
RAILS_MAX_THREADS=5

# Evolution API
AUTHENTICATION_API_KEY=$(hex 24)
DATABASE_CONNECTION_URI=postgresql://postgres:$PG@postgres:5432/evolution?schema=public
CHATWOOT_IMPORT_DATABASE_CONNECTION_URI=postgresql://postgres:$PG@postgres:5432/chatwoot?sslmode=disable

# Senhas iniciais das pessoas (trocar no primeiro acesso)
SENHA_ADMIN=Adm-$(hex 6)!
SENHA_EQUIPE=Loja-$(hex 6)!
ENV
echo ".env criado."
