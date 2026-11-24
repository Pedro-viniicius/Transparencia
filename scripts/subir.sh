#!/usr/bin/env bash
# Sobe tudo do zero (ou reaplica) e roda o teste. Idempotente.
# Uso: scripts/subir.sh            (o 1º acesso ao painel cria o administrador; ver README)
set -euo pipefail
cd "$(dirname "$0")/.."

scripts/gerar-env.sh
docker compose pull -q
docker compose up -d postgres redis

echo "Preparando o banco do Chatwoot…"
docker compose run --rm chatwoot bundle exec rails db:chatwoot_prepare >/dev/null

docker compose up -d
esperar() { for _ in $(seq 1 60); do [[ $(curl -s -o /dev/null -w '%{http_code}' "$1") == 200 ]] && return 0; sleep 2; done; echo "não respondeu: $1"; exit 1; }
esperar http://127.0.0.1:3000/api
esperar http://127.0.0.1:8080/
esperar http://127.0.0.1:8090/

if ! echo 'exit(User.where(email: "admin@lojas.local").exists? ? 0 : 1)' \
    | docker compose exec -T chatwoot bundle exec rails runner - >/dev/null 2>&1; then
  echo
  echo "Falta o administrador. Abra http://chatwoot.localhost:3000 e preencha:"
  echo "  Nome: Administrador · Empresa: Atendimento Lojas · E-mail: admin@lojas.local"
  echo "  Senha: a SENHA_ADMIN do .env  (desmarque a newsletter)"
  echo "Depois rode scripts/subir.sh de novo."
  exit 0
fi

python3 -I scripts/configurar.py
python3 -I scripts/testar.py
