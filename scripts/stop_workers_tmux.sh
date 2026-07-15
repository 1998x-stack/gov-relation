#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SESSION="${SESSION:-gov-relation-workers}"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux kill-session -t "$SESSION"
  echo "tmux session stopped: $SESSION"
else
  echo "tmux session not running: $SESSION"
fi

bash scripts/stop_workers.sh
