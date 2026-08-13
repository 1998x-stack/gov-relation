#!/usr/bin/env bash
# gov-relation batch runner v4
# No fancy tricks. One task per `opencode run` call.
# Each task self-contained with temp prompt file.

cd /workspace/data/xieming/other-codes/gov-relation || exit 1
mkdir -p logs data/database data/graph report
find /workspace/data/xieming/.local/share/opencode/snapshot -name "index.lock" -delete 2>/dev/null

log() { echo "[$(date +%H:%M:%S)] $*"; }

RN=1
while [ "$RN" -le 5 ]; do
  OUT=$(python3 run_todo_loop.py 2>&1)
  echo "$OUT" | grep -q "ALL DONE" && echo "ALL DONE!" && break

  TASK=$(echo "$OUT" | grep 'task_id:' | sed 's/.*task_id: *//')
  REG=$(echo "$OUT" | grep 'region:' | sed 's/.*region: *//')
  LEV=$(echo "$OUT" | grep 'level:' | sed 's/.*level: *//')
  PROV=$(echo "$OUT" | grep 'province:' | sed 's/.*province: *//')
  PAR=$(echo "$OUT" | grep 'parent_city:' | sed 's/.*parent_city: *//')

  log "[$RN/5] $TASK - $REG ($PROV)"

  TM=$(python3 generate_build_template.py "$TASK" 2>/dev/null)
  SCR=$(echo "$TM" | grep 'build_script:' | sed 's/.*build_script: *//')
  DB=$(echo "$TM" | grep 'db_output:' | sed 's/.*db_output: *//')
  GX=$(echo "$TM" | grep 'gexf_output:' | sed 's/.*gexf_output: *//')
  [ -z "$SCR" ] && SCR="build_auto.py"
  [ -z "$DB" ] && DB="data/database/auto.db"
  [ -z "$GX" ] && GX="data/graph/auto.gexf"
  log "  -> $SCR"

  # Write prompt to file to avoid shell expansion issues
  cat > /tmp/gov_prompt.txt << XEOF
You are a Chinese government personnel network investigator.

Working directory: /workspace/data/xieming/other-codes/gov-relation

Investigate leadership team of ${REG} (${LEV}) in ${PROV}. Parent city: ${PAR}. Task: ${TASK}.

Process:
1. WebSearch for resumes of the party secretary and government head
2. WebSearch for leadership roster, predecessor info, cross-county exchanges
3. Deep dive into gaps
4. Generate build script ${SCR} with hardcoded data:
   - persons, organizations, positions, relationships lists
   - SQLite DB -> ${DB}
   - GEXF graph -> ${GX} (string concat, red=secretary blue=gov orange=other)
5. Run: python3 ${SCR}
6. Mark done: python3 run_todo_loop.py --mark-done ${TASK}

Rules: cite sources, flag gaps, use WebSearch + WebFetch. gov sites > Baidu Baike > news.
XEOF

  LOG="logs/${TASK}.log"
  log "  running opencode..."
  opencode run "$(cat /tmp/gov_prompt.txt)" \
    -m iagent/standard \
    --variant ulw \
    --dir . \
    --print-logs \
    > "$LOG" 2>&1
  EC=$?
  log "  exit=$EC log=$(wc -c < "$LOG")b"

  python3 run_todo_loop.py --mark-done "$TASK" 2>&1 | log
  RN=$((RN + 1))
done

log "===== Batch done: $((RN-1)) items ====="
python3 run_todo_loop.py --status 2>&1
