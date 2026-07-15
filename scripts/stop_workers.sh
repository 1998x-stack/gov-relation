#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LOG_DIR="${LOG_DIR:-logs/workers}"

if [[ ! -d "$LOG_DIR" ]]; then
  echo "No worker log directory: $LOG_DIR"
  exit 0
fi

for pid_file in "$LOG_DIR"/*.pid; do
  [[ -e "$pid_file" ]] || continue
  pid="$(cat "$pid_file")"
  worker="$(basename "$pid_file" .pid)"
  if kill -0 "$pid" 2>/dev/null; then
    echo "Stopping ${worker} pid=${pid}"
    kill "$pid" || true
  else
    echo "${worker} not running"
  fi
  rm -f "$pid_file"
done

python3 scripts/todo_queue.py status

