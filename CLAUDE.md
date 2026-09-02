# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A research pipeline for investigating government officials' career histories and building personnel relationship networks (who-knows-who, co-working, succession, cross-region transfers). Output targets: SQLite databases, GEXF graph files, person-profile JSON, and Markdown/HTML reports. The system is a "research pipeline," not a traditional application — it produces structured data through regional build scripts, a unified platform database, and a local read-only web UI.

## Key commands

```bash
# Test suite
python3 -m pytest tests/                       # full suite
python3 -m pytest tests/test_runner.py -v      # single module

# Inventory: audit scripts, databases, graphs, missing pairs
python3 scripts/inventory.py

# TODO queue: see progress, next task, mark done
python3 scripts/tools/run_todo_loop.py --status
python3 scripts/tools/run_todo_loop.py
python3 scripts/tools/run_todo_loop.py --mark-done <task_id>

# Concurrent worker queue
python3 scripts/todo_queue.py claim --worker-id w1 --model standard
python3 scripts/todo_queue.py status
python3 scripts/todo_queue.py done --task-id <id> --worker-id <id>

# Dispatch: generate an investigation prompt for the next TODO item
python3 scripts/dispatch_todo.py --next --model standard

# Validate and promote staged tmp artifacts (dry-run first, then --apply)
python3 scripts/process_tmp.py data/tmp/<task_id>
python3 scripts/process_tmp.py data/tmp/<task_id> --apply

# Unified platform database (build, audit, commercial-release check)
python3 scripts/govdb.py build --database data/platform/gov_relation.db [--replace]
python3 scripts/govdb.py audit --database data/platform/gov_relation.db

# Local read-only API + static UI: http://127.0.0.1:8000/app.html
python3 scripts/serve_app.py --port 8000

# Refresh GitHub Pages static data
python3 scripts/build_static_site_data.py

# Nohup workers (4 workers, auto-done + git-commit)
bash scripts/start_workers_nohup.sh
bash scripts/worker_status.sh
bash scripts/stop_workers.sh
```

## Architecture

### Data pipeline layers

1. **Research** — `data/TODO.json` (~3100 tasks across all provinces) drives the queue. Workers claim tasks, investigate officials, stage output in `data/tmp/<task_id>/`.
2. **Validate & promote** — `scripts/process_tmp.py` validates staged artifacts and copies them into canonical directories (`data/database/`, `data/graph/`, `data/persons/`, `report/`).
3. **Ingest** — `scripts/govdb.py build` losslessly imports all SQLite databases and person JSON into the unified platform database (`data/platform/gov_relation.db`) with bronze/silver/evidence/quality/gold data layers.
4. **Resolve** — Conservative deterministic entity resolution (match on normalized name + birth; false separation preferred over false merge). Ambiguous identities enter `resolution_candidates`.
5. **Serve** — `scripts/serve_app.py` provides a read-only API over SQLite databases. GitHub Pages from `docs/`.

### Shared Python package (`gov_relation/`)

| Module | Role |
|---|---|
| `paths.py` | All path constants: `DATABASE_DIR`, `GRAPH_DIR`, `PERSONS_DIR`, `CANONICAL_DB`, `TODO_PATH`, `DISPATCH_STATE_PATH`, etc. Uses `pathlib.Path`. |
| `schema.py` | Unified SQLite `CREATE TABLE` and batch-insert functions for persons, organizations, positions, relationships. |
| `gexf.py` | `GEXFBuilder` — programmatic GEXF XML generation with nodes, edges, and visual attributes. |
| `runner.py` | `run_build()` — top-level orchestrator: create tables → insert data → write GEXF → optionally sync to central registry. This is the canonical entry point for new regional builders. |
| `colors.py` | Node color/size/shape rules for graph visualization. |
| `todo.py` | `TODO.json` read/write, traverse, stats, mark-done. |
| `queue.py` | File-lock-based concurrent claim/done/fail/release for `data/dispatch_state.json`. |
| `inventory.py` | Read-only scan of scripts, databases, GEXF files, reports; identifies missing artifact pairs. |
| `log.py` | Unified logging with rotation and formatting. |
| `slugs.py` | Chinese region name → file-safe slug mapping. |
| `dispatch.py` | Prompt generation from TODO items. |
| `web.py` | Read-only SQLite/GEXF API endpoints used by `serve_app.py`. |
| `central.py` | Cross-region registry writer (merge persons/orgs across builds). |

### Platform sub-package (`gov_relation/platform/`)

The v2 data platform implementing bronze/silver/gold layered architecture (see `docs/ARCHITECTURE_V2.md`):
- `schema.py` — canonical DDL for all layers
- `importer.py` — lossless SQLite + person-JSON import
- `identity.py` / `resolution.py` — conservative deterministic entity resolution
- `quality.py` — quality issues and resolution candidates quarantine
- `rights.py` — source rights tracking; commercial export gating

### Build script conventions

New regional scripts live in `scripts/build/build_<slug>_data.py`. Root-level `build_*_data.py` files are legacy. Every builder embeds four data lists (`persons`, `organizations`, `positions`, `relationships`) and calls `gov_relation.runner.run_build()`. Output naming: `<slug>_network.db` + `<slug>_network.gexf`.

### Concurrent queue design

`scripts/todo_queue.py` uses a lock directory (`data/dispatch_state.lock`) to prevent multiple workers from claiming the same task. State is tracked in `data/dispatch_state.json`. Workers are typically run via `start_workers_nohup.sh` (4 nohup OpenCode processes), each writing to `logs/workers/worker-N.log`.

### Staging area (`data/tmp/`)

All new investigation output goes here first. Supported files: `build_<slug>_data.py`, `<slug>_network.db`, `<slug>_network.gexf`, person JSON profiles (`YYYYMMDD-{province}-{city}-{job}-{name}.json`), and Markdown/HTML reports. `scripts/process_tmp.py` validates and promotes to canonical directories.

## Personnel research skill

The project skill for investigation lives at `.agents/skills/china-gov-network/SKILL.md`. When doing personnel research, use the `china-gov-network` skill via `Skill` tool — it governs how to investigate officials' resumes, build databases, and generate reports.

## Coding conventions

- Python 3.11, four-space indentation, `snake_case`, type hints, `pathlib.Path`
- Prefer stdlib. No formatter/linter/type checker configured — keep changes PEP 8-compatible
- New builders must use `gov_relation.runner.run_build()` and paths from `gov_relation.paths`
- Tests: `tests/test_<module>.py`, `Test...` classes, `test_<behavior>` methods, `tmp_path` for isolation
- Commit style: `Complete gov relation task <task_id>` for investigation promotions; `fix(worker): ...` for fixes
- Never commit `opencode.jsonc`, worker logs, PID/lock files, or generated artifacts that belong in `.gitignore`
- The repo contains legacy root-level `build_*_data.py` scripts with hardcoded absolute paths — do not replicate this pattern; new scripts go in `scripts/build/` and use `gov_relation.paths`
