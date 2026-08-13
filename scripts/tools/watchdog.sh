#!/usr/bin/env bash
# watchdog.sh — auto-manage todo_batch for gov-relation
# - If batch not running and items remain → start it
# - If batch stuck (>15min no new log) → kill and restart
# - Saves status for monitoring
BASE="/workspace/data/xieming/other-codes/gov-relation"
STATUS_FILE="$BASE/logs/watchdog_status.txt"
LOG_DIR="$BASE/logs"
PID_FILE="$LOG_DIR/batch.pid"
BATCH_SCRIPT="$BASE/todo_batch.sh"

mkdir -p "$LOG_DIR"
cd "$BASE"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

# TODO status
TODO_STATUS="$(python3 run_todo_loop.py --status 2>&1)"
REMAINING="$(echo "$TODO_STATUS" | grep 'Remaining:' | grep -oP '\d+')"
DONE="$(echo "$TODO_STATUS" | grep 'Finished:' | grep -oP '\d+')"
PCT="$(echo "$TODO_STATUS" | grep 'Progress:' | grep -oP '[\d.]+(?=%)')"

# Check if batch is running
BATCH_PID=""
if [ -f "$PID_FILE" ]; then
  BPID="$(cat "$PID_FILE")"
  if kill -0 "$BPID" 2>/dev/null; then
    BATCH_PID="$BPID"
  fi
fi

# Also find by process name
if [ -z "$BATCH_PID" ]; then
  BP="$(pgrep -f "todo_batch.sh" 2>/dev/null | head -1)"
  [ -n "$BP" ] && kill -0 "$BP" 2>/dev/null && BATCH_PID="$BP"
fi

if [ -n "$BATCH_PID" ]; then
  echo "$TIMESTAMP | RUNNING | PID=$BATCH_PID | Done=$DONE | Remaining=$REMAINING | ${PCT}%" > "$STATUS_FILE"
  # Check if log activity is stale (>20min)
  LATEST_LOG="$(ls -t "$LOG_DIR"/*.log 2>/dev/null | head -1)"
  if [ -n "$LATEST_LOG" ]; then
    LOG_AGE=$(( $(date +%s) - $(stat -c %Y "$LATEST_LOG") ))
    if [ "$LOG_AGE" -gt 1500 ]; then
      echo "$TIMESTAMP | ⚠️ STALE (${LOG_AGE}s) — killing & restarting" >> "$STATUS_FILE"
      kill "$BATCH_PID" 2>/dev/null
      sleep 2
      # Clean old snapshot locks
      find /workspace/data/xieming/.local/share/opencode/snapshot -name "index.lock" -delete 2>/dev/null
      LOGFILE="$LOG_DIR/batch_$(date +%Y%m%d_%H%M%S).log"
      nohup bash "$BATCH_SCRIPT" > "$LOGFILE" 2>&1 &
      echo "$!" > "$PID_FILE"
      echo "$TIMESTAMP | ✅ RESTARTED PID=$! → $LOGFILE" >> "$STATUS_FILE"
    fi
  fi
else
  if [ "$REMAINING" -gt 0 ] 2>/dev/null; then
    # Clean snapshot locks before starting
    find /workspace/data/xieming/.local/share/opencode/snapshot -name "index.lock" -delete 2>/dev/null
    LOGFILE="$LOG_DIR/batch_$(date +%Y%m%d_%H%M%S).log"
    nohup bash "$BATCH_SCRIPT" > "$LOGFILE" 2>&1 &
    echo "$!" > "$PID_FILE"
    echo "$TIMESTAMP | STOPPED→STARTED | PID=$! | Done=$DONE | Remaining=$REMAINING | ${PCT}%" > "$STATUS_FILE"
    echo "$TIMESTAMP | Log: $LOGFILE" >> "$STATUS_FILE"
  else
    echo "$TIMESTAMP | ALL DONE! | Done=$DONE | Remaining=0 | 100.0%" > "$STATUS_FILE"
  fi
fi
