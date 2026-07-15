#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SESSION="${SESSION:-gov-relation-workers}"
LOG_DIR="${LOG_DIR:-logs/workers}"
mkdir -p "$LOG_DIR"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already running: $SESSION"
  tmux list-sessions | grep "^${SESSION}:"
  exit 0
fi

tmux new-session -d -s "$SESSION" -c "$ROOT" \
  "bash scripts/start_workers_nohup.sh; echo '[tmux] worker launcher exited; keeping session alive'; while true; do sleep 3600; done"

echo "tmux session started: $SESSION"
tmux list-sessions | grep "^${SESSION}:"
