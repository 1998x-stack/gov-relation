# Repository Guidelines

## Project Structure & Module Organization

`gov_relation/` is the shared Python package; `gov_relation/platform/` owns the canonical v2 schema, import, resolution, and quality gates. Put new regional generators in `scripts/build/build_<slug>_data.py`; root-level `build_*_data.py` files are legacy and should not be copied. Operational tools live in `scripts/`, tests in `tests/`, and the GitHub Pages site in `docs/`. See `docs/ARCHITECTURE_V2.md` for the target architecture, and `docs/CANONICAL_JSONL_ARCHITECTURE.md` for the new data-layer model.

## Canonical data layer (JSONL + SQLite backup)

The data layer follows a **canonical JSONL + SQLite-backup** model (destructive refactor, step 2 done):

- **`data/records/*.jsonl` is the single system of record** — one JSON object per line, per entity stream (`persons`, `organizations`, `positions`, `relationships`, `sources`, `claims`, `profile_documents`, ...), content-addressed via `manifest.json` (counts + sha256).
- **`data/database/platform.db` is a derived SQLite backup** rebuilt from the JSONL by `python3 scripts/gov2.py backup`; it is disposable and never edited directly.
- **`gov2 verify` guarantees the two are byte-for-byte identical** (run after any change).
- Pillars: `gov2 build` (data generation), `gov2 viz` (visualization), `gov2 classify` (classification/induction), `gov2 profiles` (ingest person profiles), `gov2 export` (SQLite→JSONL).
- **Region generation (step 3):** new/imigrated regional `build_*_data.py` use `backend="canon"` in `run_build`, which writes `data/records/regions/<province>__<slug>/*.jsonl` (partitioned, region-scoped ids). Aggregate and publish with:

```bash
python3 scripts/gov2.py region --spec <spec.json> --slug <区> --province <省>   # (optional) spec entry
python3 scripts/gov2.py snapshot --records data/records   # merge partitions -> unified streams
python3 scripts/gov2.py backup data/records data/database/platform.db --overwrite
python3 scripts/gov2.py verify data/records data/database/platform.db
```
- Git strategy: `data/records/regions/**` (partitioned region JSONL) is committed; the unified flat streams `data/records/*.jsonl` and the SQLite backup are ignored/regenerated (`gitignore` covers both).
- Legacy SQLite/person/graph/report artifacts were archived to `.trash_batch/legacy_20260902/` (recoverable) rather than deleted; the legacy `platform`, `database`, `graph`, `persons`, `provinces`, `report`, `research_output` paths are no longer the active data layer.

```bash
python3 scripts/gov2.py verify data/records data/database/platform.db   # consistency gate
python3 scripts/gov2.py backup data/records data/database/platform.db --overwrite
python3 scripts/gov2.py classify --records data/records                # Pillar C
python3 scripts/gov2.py viz --records data/records                    # Pillar B
```

## Build, Test, and Development Commands

```bash
python3 -m pytest tests/                       # run the full unit suite
python3 -m pytest tests/test_runner.py -v      # run one test module
python3 scripts/inventory.py                   # audit scripts and artifacts
python3 scripts/build_static_site_data.py      # refresh Pages data
python3 scripts/serve_app.py --port 8000       # serve the read-only local UI
python3 scripts/todo_queue.py status           # inspect worker queue state
python3 scripts/govdb.py audit                 # audit canonical data quality and rights
```

Validate staged investigation output with `python3 scripts/process_tmp.py data/tmp/<task_id>`; add `--apply` only after the dry run succeeds.

## Coding Style & Naming Conventions

Use Python 3.11 syntax, four-space indentation, `snake_case` names, type hints, `pathlib.Path`, and concise module docstrings. Follow existing import grouping and prefer stdlib-only implementations. There is no configured formatter, linter, or type checker, so keep changes PEP 8-compatible and review diffs manually. New builders must call `gov_relation.runner.run_build()` and write `<slug>_network.db` plus `<slug>_network.gexf` through paths from `gov_relation.paths`.

## Testing Guidelines

Pytest tests follow `tests/test_<module>.py`; use `Test...` classes and `test_<behavior>` methods. Add regression tests for library or pipeline changes and use `tmp_path` for filesystem/database isolation. No coverage threshold is configured, but run the full suite before submitting. For UI changes, rebuild static data, preview the site locally, and include a screenshot when appearance changes.

## Investigation & Data Safety

For personnel research, follow `.agents/skills/china-gov-network/SKILL.md`. Stage all new artifacts in `data/tmp/<task_id>/`, validate, promote, then rerun inventory. Do not invoke queue `claim`, `done`, `fail`, or `fillet` from externally dispatched agent tasks. Never commit `opencode.jsonc`, worker logs, PID/lock files, or unrelated generated artifacts.

## Commit & Pull Request Guidelines

History uses imperative subjects such as `fix(worker): ...` and automated `Complete gov relation task <task_id>`. Keep commits focused and use the task form for investigation promotions. PRs should explain scope, list verification commands, identify affected datasets/artifacts and public sources, link the task or issue, and call out schema or generated-site changes.
