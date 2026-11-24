#!/usr/bin/env bash
# Backup dos dois bancos + sessões do WhatsApp + anexos. Serve para migrar para o servidor.
# Uso: scripts/backup.sh  → backups/AAAA-MM-DD_HHMM/
set -euo pipefail
cd "$(dirname "$0")/.."
destino="backups/$(date +%F_%H%M)"
mkdir -p "$destino"
umask 077
for banco in chatwoot evolution; do
  docker compose exec -T postgres pg_dump -U postgres -Fc "$banco" > "$destino/$banco.dump"
done
docker compose exec -T evolution tar -C /evolution -czf - instances > "$destino/evolution-instances.tgz"
docker compose exec -T chatwoot tar -C /app -czf - storage > "$destino/chatwoot-storage.tgz"
cp .env "$destino/env"
ls -lh "$destino"
echo "Backup em $destino (contém segredos: guarde com cuidado)."
