#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LOG_DIR="${LOG_DIR:-logs/workers}"

echo "== Process status =="
if [[ -d "$LOG_DIR" ]]; then
  for pid_file in "$LOG_DIR"/*.pid; do
    [[ -e "$pid_file" ]] || continue
    pid="$(cat "$pid_file")"
    worker="$(basename "$pid_file" .pid)"
    if kill -0 "$pid" 2>/dev/null; then
      echo "RUNNING ${worker} pid=${pid}"
    else
      echo "STOPPED ${worker} pid=${pid}"
    fi
  done
else
  echo "No worker log directory: $LOG_DIR"
fi

echo
echo "== Queue status =="
python3 scripts/todo_queue.py status

echo
echo "== Recent logs =="
if [[ -d "$LOG_DIR" ]]; then
  for log_file in "$LOG_DIR"/*.log; do
    [[ -e "$log_file" ]] || continue
    echo "--- ${log_file} ---"
    tail -n 8 "$log_file" || true
  done
fi
