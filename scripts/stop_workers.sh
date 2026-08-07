#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LOG_DIR="${LOG_DIR:-logs/workers}"

if [[ ! -d "$LOG_DIR" ]]; then
  echo "No worker log directory: $LOG_DIR"
  exit 0
fi

# Workers are `setsid`-launched so PGID == supervisor PID; kill the group to
# reap the `opencode run` child instead of orphaning it to PID 1.
for pid_file in "$LOG_DIR"/*.pid; do
  [[ -e "$pid_file" ]] || continue
  pid="$(cat "$pid_file")"
  worker="$(basename "$pid_file" .pid)"
  if kill -0 "$pid" 2>/dev/null; then
    echo "Stopping ${worker} pid=${pid} (process group)"
    kill -- -"$pid" 2>/dev/null || kill "$pid" || true
    for _ in 1 2 3 4 5 6 7 8; do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.5
    done
    kill -9 -- -"$pid" 2>/dev/null || true
  else
    echo "${worker} not running"
  fi
  rm -f "$pid_file"
done

# Reap agents orphaned by supervisors that died before this stop ran.
while read -r agent_pid; do
  [[ -n "$agent_pid" ]] || continue
  echo "Stopping orphaned agent pid=${agent_pid}"
  kill "$agent_pid" 2>/dev/null || true
done < <(pgrep -f "opencode run --model .*task_id:" || true)

python3 scripts/todo_queue.py status

