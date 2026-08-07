# AGENTS.md — gov-relation

Chinese government personnel career histories, leadership rosters, relationship networks, and cross-region cadre transfer research.

## Quick start

```bash
python3 -m pytest tests/                 # 162 tests, stdlib only
python3 scripts/inventory.py             # count scripts, DBs, GEXFs
python3 scripts/serve_app.py --port 8000   # read-only local API + docs/
```

## Test & verify

- **Run all tests**: `python3 -m pytest tests/` (no deps beyond stdlib + pytest)
- **Run a single file**: `python3 -m pytest tests/test_runner.py -v`
- All scripts launch via `sys.path.insert(0, ...)` to `import gov_relation`
- CI: GitHub Pages only (`.github/workflows/pages.yml`) — no lint/typecheck

## Build scripts — two lives

| Location | Count | When to use |
|---|---|---|
| `build_*_data.py` (repo root) | ~100 old-style | Pre-existing, do not replicate |
| `scripts/build/build_*_data.py` | newer | **All new scripts go here** |

New build scripts should use the shared `gov_relation.runner.run_build()` API:

```python
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

run_build(
    slug="七里河区",
    persons=[...],
    organizations=[...],
    positions=[...],
    relationships=[...],
    db_path=DATABASE_DIR / "七里河区_network.db",
    gexf_path=GRAPH_DIR / "七里河区_network.gexf",
)
```

## Queue-driven worker pipeline

`data/TODO.json` is the source of truth for ~3100 investigation tasks.

- **Claim a task**: `python3 scripts/todo_queue.py claim --worker-id foo`
- **Status**: `python3 scripts/todo_queue.py status`
- **Concurrency**: Lock file at `data/dispatch_state.lock`, state at `data/dispatch_state.json`
- **Start 4 workers**: `nohup bash scripts/start_workers_nohup.sh > logs/workers/supervisor.log 2>&1 &`
- Worker loop: `python3 scripts/worker_loop.py`
- Stopping: `bash scripts/stop_workers.sh`
- Each worker gets a generated prompt via `scripts/dispatch_todo.py` and `gov_relation.dispatch.build_dispatch_prompt()`
- Tasks used externally — do NOT call `claim/done/fail/fillet` from agent task code
- After verification and promotion (`scripts/process_tmp.py data/tmp/<tid> --apply`), `AUTO_DONE=1 GIT_COMMIT=1` auto-commits

## Investigation work (for new tasks)

- **Use the china-gov-network skill**: `.agents/skills/china-gov-network/SKILL.md` — it defines the full investigation workflow
- **Staging-first workflow**: write artifacts to `data/tmp/<task_id>/`, validate with `scripts/process_tmp.py`, promote with `--apply`, then `python3 scripts/inventory.py`
- **Build script goes to**: `scripts/build/build_<slug>_data.py`
- **DB**: `data/database/<slug>_network.db`
- **GEXF**: `data/graph/<slug>_network.gexf`
- **Person JSON**: `data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json`

## Core library (`gov_relation/`)

| Module | Purpose |
|---|---|
| `runner.py` | `run_build()` — top-level orchestration for one region |
| `schema.py` | SQLite DDL + bulk-inserts for the 4 standard tables |
| `central.py` | Province-partitioned hash-based dedup (SHA256 keyed by name+birth / province+fqn) |
| `gexf.py` | `GEXFBuilder` — incremental graph builder |
| `colors.py` | Node color/size/shape rules by title |
| `hash.py` | `person_hash(name, birth)` / `org_hash(province, fqn)` |
| `paths.py` | `REPO_ROOT`, `DATABASE_DIR`, `GRAPH_DIR`, etc. |
| `todo.py` | `data/TODO.json` reader/writer |
| `queue.py` | Concurrent queue state with lock-based mutex |
| ` dispatch.py` | Generate investigation prompt from TODO item |
| ` slugs.py` | Chinese region → filename slug mapping |
| `inventory.py` | Count build_scripts, DBs, GEXFs, orphans |
| `province.py` | Resolve province from region slug via TODO.json |
| `web.py` | Read-only local API (`/api/databases`, `/api/database/<name>`) + static HTML dashboard |
| `log.py` | Unified logging with RotatingFileHandler |

## Gotchas

- **`opencode.jsonc`** is in `.gitignore` — do not check it in
- **`package.json`**: only Playwright for tests; there's no Node.js application code
- **Import path**: scripts use `sys.path.insert(0, str(Path(__file__).resolve().parents[1]))` before `import from gov_relation`
- Some scripts still use `build_data.py` conventions with direct DB writes instead of `runner.run_build()`