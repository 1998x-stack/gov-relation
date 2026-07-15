#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

WORKER_COUNT="${WORKER_COUNT:-4}"
MAX_TASKS="${MAX_TASKS:-0}"
SLEEP_SECONDS="${SLEEP_SECONDS:-30}"
OPENCODE_BIN="${OPENCODE_BIN:-opencode}"
OPENCODE_AGENT="${OPENCODE_AGENT:-general}"
LOG_DIR="${LOG_DIR:-logs/workers}"
AUTO_DONE="${AUTO_DONE:-1}"
GIT_COMMIT="${GIT_COMMIT:-1}"
OPENCODE_AUTO="${OPENCODE_AUTO:-1}"

mkdir -p "$LOG_DIR" logs/dispatch data/tmp

start_worker() {
  local id="$1"
  local model_intent="$2"
  local opencode_model="$3"
  local worker_id="worker-${id}"
  local log_file="${LOG_DIR}/${worker_id}.log"
  local pid_file="${LOG_DIR}/${worker_id}.pid"

  if [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
    echo "${worker_id} already running pid=$(cat "$pid_file")"
    return 0
  fi

  local args=(
    python3 scripts/worker_loop.py
    --worker-id "$worker_id"
    --model-intent "$model_intent"
    --execute
    --opencode-bin "$OPENCODE_BIN"
    --opencode-agent "$OPENCODE_AGENT"
    --opencode-model "$opencode_model"
    --max-tasks "$MAX_TASKS"
    --sleep-seconds "$SLEEP_SECONDS"
  )
  if [[ "$AUTO_DONE" == "1" ]]; then
    args+=(--auto-done)
  fi
  if [[ "$GIT_COMMIT" == "1" ]]; then
    args+=(--git-commit)
  fi
  if [[ "$OPENCODE_AUTO" == "1" ]]; then
    args+=(--opencode-auto)
  fi

  echo "Starting ${worker_id} intent=${model_intent} agent=${OPENCODE_AGENT} model=${opencode_model} log=${log_file}"
  {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] START ${worker_id} intent=${model_intent} agent=${OPENCODE_AGENT} model=${opencode_model} max_tasks=${MAX_TASKS} auto_done=${AUTO_DONE} git_commit=${GIT_COMMIT} opencode_auto=${OPENCODE_AUTO} opencode=${OPENCODE_BIN}"
  } >>"$log_file"
  nohup env PYTHONUNBUFFERED=1 "${args[@]}" >>"$log_file" 2>&1 &
  echo "$!" >"$pid_file"
}

for i in $(seq 1 "$WORKER_COUNT"); do
  model_var="MODEL_${i}"
  if [[ -n "${!model_var:-}" ]]; then
    opencode_model="${!model_var}"
    if [[ "$opencode_model" == iagent/* ]]; then
      model_intent="iagent"
    else
      model_intent="standard"
    fi
  else
    model_intent="iagent"
    opencode_model="iagent/standard"
  fi
  start_worker "$i" "$model_intent" "$opencode_model"
done

python3 scripts/todo_queue.py status
