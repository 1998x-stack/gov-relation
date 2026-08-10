#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
COMPOSE_FILE="$REPO_ROOT/infra/postgres/compose.yml"
MIGRATION_DIR="$REPO_ROOT/migrations/postgres"
COMPOSE=(docker compose -p gov-relation -f "$COMPOSE_FILE")
DB_NAME=${GOV_RELATION_POSTGRES_DB:-gov_relation}
DB_USER=${GOV_RELATION_POSTGRES_USER:-gov_relation}

usage() {
    echo "Usage: $0 {up|status|migrate|verify|down}" >&2
}

psql_exec() {
    "${COMPOSE[@]}" exec -T postgres psql -X -v ON_ERROR_STOP=1 -U "$DB_USER" -d "$DB_NAME" "$@"
}

wait_ready() {
    local attempt
    for attempt in $(seq 1 30); do
        if "${COMPOSE[@]}" exec -T postgres pg_isready -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
    done
    echo "PostgreSQL did not become ready" >&2
    return 1
}

apply_migrations() {
    local file version checksum table_exists existing
    wait_ready
    for file in "$MIGRATION_DIR"/[0-9][0-9][0-9][0-9]_*.sql; do
        version=$(basename "$file" | cut -d_ -f1)
        checksum=$(sha256sum "$file" | cut -d' ' -f1)
        table_exists=$(psql_exec -Atc "SELECT to_regclass('meta.schema_migrations') IS NOT NULL")
        existing=""
        if [[ "$table_exists" == "t" ]]; then
            existing=$(psql_exec -Atc "SELECT checksum FROM meta.schema_migrations WHERE version='$version'")
        fi
        if [[ -n "$existing" ]]; then
            if [[ "$existing" != "$checksum" ]]; then
                echo "Checksum mismatch for migration $version" >&2
                return 1
            fi
            echo "skip $version (already applied)"
            continue
        fi
        echo "apply $(basename "$file")"
        psql_exec -v migration_checksum="$checksum" -f "/migrations/$(basename "$file")"
    done
}

case "${1:-}" in
    up)
        "${COMPOSE[@]}" up -d postgres
        wait_ready
        ;;
    status)
        "${COMPOSE[@]}" ps
        ;;
    migrate)
        apply_migrations
        ;;
    verify)
        wait_ready
        psql_exec -f /migrations/verify/0001_registry_and_assertions.sql
        ;;
    down)
        "${COMPOSE[@]}" down
        ;;
    *)
        usage
        exit 2
        ;;
esac
