# SubAgentReview — Phase 4 (新流程上线) — 2026-08-11

Reviewer: SubAgentReview (adversarial, code-verified, no trust in checkboxes)
Scope: Plan `docs/superpowers/plans/2026-08-10-v3-phase3-5-migration.md` §Phase 4,
spec `docs/superpowers/specs/2026-08-10-v3-refactor-design.md` §4.5/4.6/§10,
commits `2e2385525`, `38a93c8df`, `8086baaa4`, `e6883c9b8`.
Read-only: no edits/commits made. Working-tree dirtiness from other lanes noted but ignored.

## Commands run (evidence base)

```bash
git log --oneline -15 / git status --short
git show --stat {2e2385525,38a93c8df,8086baaa4,e6883c9b8}
git show 38a93c8df -- gov_relation/dispatch.py gov_relation/queue.py tests/test_dispatch.py tests/test_queue.py
git show 8086baaa4 -- gov_relation/central.py scripts/tools/{run_todo_loop,generate_build_template}.py gov_relation/platform/rights.py tests/test_rights.py
python3 -m pytest tests/test_process_tmp_province.py tests/test_dispatch.py tests/test_queue.py -q   # 38 passed
python3 -m pytest tests/test_process_tmp_province.py -q   # 5 passed
python3 -m pytest tests/test_dispatch.py -q   # 11 passed
python3 -m pytest tests/test_queue.py -q      # 22 passed
python3 -m pytest tests/ -q                   # 243 passed, 1 warning
find data/provinces/guangxi -maxdepth 3; git ls-files scripts/build/ | grep -i guangxi; git check-ignore -v ...
sqlite3: PRAGMA foreign_key_check + COUNT(*) per table on both sample DBs
python3 scripts/process_tmp.py guangxi_南丹县   # live dry-run via root wrapper
python3 -c "...canonical_artifacts_ready({task_id/region/province})..."   # live queue readiness
cd /tmp && python3 .../scripts/tools/run_todo_loop.py --help; .../generate_build_template.py --help; .../scripts/process_tmp.py --help
grep -rn "data/database\|data/graph\|data/persons" gov_relation/dispatch.py gov_relation/queue.py tests/test_{dispatch,queue,process_tmp_province}.py
python3 -c "warnings.simplefilter('error', DeprecationWarning); import gov_relation.central"
```

## Per-item verdicts

### A. process_tmp province routing — PASS (2 minor notes)

- `destinations_for()` (`.agents/skills/china-gov-network/scripts/process_tmp.py`) calls
  `find_item_by_id(load_todo(), staging_dir.name)`; known task → `province_database/graph/persons/reports_dir`,
  unknown → `dict(DESTINATIONS)` + `"legacy-fallback"`. ✅ single resolver drives both dry-run and `--apply`
  (both go through `collect_actions()`; no duplicated path logic — verified by reading).
- `gov_relation/todo.py`: `TodoItem.province_name` field ✅, `find_item_by_id()` exists ✅.
- Root wrapper `scripts/process_tmp.py` delegates via `runpy.run_path` → correct target path
  (`parents[1]/.agents/.../process_tmp.py`); REPO_ROOT inside child == repo root (parents[4]).
  ✅ **Live test**: `python3 scripts/process_tmp.py guangxi_南丹县` (dry run) routed
  person_json/report/database/graph → `data/provinces/guangxi/{persons,reports,database,graph}`,
  build_script → `scripts/build/`, `route=广西壮族自治区`; `find_item_by_id` resolves the id.
- Tests: `tests/test_process_tmp_province.py` = **5 passed** (known route, unknown fallback,
  todo-error propagation, checkpoint-not-promoted, WAL no sidecars). ⚠️ Notes:
  1. Plan/completion record claim **6 例**; file contains **5** test functions.
  2. Plan-specified behavior **“同名目标拒绝覆盖”** (overwrite refusal) is implemented in
     `promote()` (`FileExistsError`) but has **no dedicated test**; “PersonJSONFactory 输出可被 classify”
     also has no direct unit test (validated empirically via the live dry-run classify of real v3
     Person JSONs). “dry-run 不写入” is covered by pre-existing `tests/test_process_tmp.py::test_dry_run_keeps_staging`.

### B. dispatch prompt (Task 2) — PASS (1 note)

- `build_dispatch_prompt` emits canonical verify block with **relative** paths:
  `scripts/build/<name>`, `data/provinces/<slug>/database/...`, `/graph/...`, persons dir. ✅
- Legacy “Canonical destination after validation: build_script/database/gexf/person_json_dir” block is
  GONE from source and from runtime prompt (grep + live print: `legacy leakage: False`). Test asserts
  `"Canonical destination after validation:\n- build_script:" not in prompt`. ✅
- “Province-aware promotion destinations” block appended (build_script_dir + database/graph/persons/report).
  No duplicate/conflicting canonical claims — single authoritative statement: canonical destination is
  selected by process_tmp.py from task_id. ✅
- `tests/test_dispatch.py` + `tests/test_queue.py`: 33 passed, updated assertions use province paths,
  no legacy canonical paths. ✅
- ⚠️ Note: the appended block renders **absolute** paths (`/workspace/data/xieming/.../data/provinces/...`)
  because province_*_dir are f-string’d without `.relative_to(REPO_ROOT)`, while the canonical block is
  relative. Functionally fine for an LLM executor, but leaks absolute machine paths and is inconsistent
  formatting.

### C. Queue readiness (Task 2 companion) — PASS

- `_canonical_artifacts_ready_unlocked`: build candidates = `scripts/build/<slug-name>.py` AND
  `scripts/build/build_<task_id>_data.py`; db/graph candidates = province path inserted at index 0,
  legacy `data/database`+`data/graph` fallback stays. ✅
- **Live check**: task `guangxi_南丹县` → `canonical_artifacts_ready(...) = (True, [])` — the
  task_id-derived build name `build_guangxi_南丹县_data.py` matches the actual committed generator,
  so province-routed artifacts satisfy the readiness gate end-to-end. ✅

### D. E2E validation (Task 3) — PASS

- Artifacts on disk (both samples) under `data/provinces/guangxi/`:
  - 南丹县: `database/南丹县_network.db`, `graph/南丹县_network.gexf`,
    persons/`20260811-广西壮族自治区-河池市-南丹县-{县委书记-黄建辉,县长-闻飞熊}.json`,
    reports/`20260811-广西壮族自治区-河池市-南丹县-领导班子增量报告.md` ✅
  - 大化瑶族自治县: db + gexf + 2 Person JSON + reports md ✅
- SQLite: `PRAGMA foreign_key_check` → `[]` on both. Counts match the plan record for 南丹县 exactly:
  persons 2, orgs 7, positions 7, relationships 1; 大化: 4/4/6/3. ✅
- Generators committed: `scripts/build/build_guangxi_南丹县_data.py` and
  `build_guangxi_大化瑶族自治县_data.py` (both in git ls-files, via Phase-1 commit 276320464). ✅
- gitignore policy honored: `.gitignore:46` `data/provinces/**` + negations
  (`!data/provinces/**/`, `!data/provinces/**/.gitkeep`); only `.gitkeep`s are tracked. ✅

### E. Regression — PASS

- Full suite: **243 passed, 1 warning** (exactly the plan’s expected count).
- The 3 PHP-protected commits + docs commit exist with file lists matching the plan:
  - `2e2385525`: skill process_tmp.py + tests/test_process_tmp_province.py ✅
  - `38a93c8df`: dispatch.py + queue.py + test_dispatch.py + test_queue.py ✅
  - `8086baaa4`: central.py, platform/rights.py, generate_build_template.py, run_todo_loop.py, test_rights.py ✅
  - `e6883c9b8`: plan doc completion notes ✅
- No Phase-4 file is dirty (git status of the affected paths is empty; staged data/../reports +
  unrelated build_* script edits from other lanes only). ✅
- rights.py v3 sync (`commercial_use=` column) matches updated schema (schema gate)=tests pass. ✅

### F. Gaps / risks (reviewed, no blockers)

1. **central.py module-level `DeprecationWarning`** fires at import time; importers:
   `tests/test_central.py`, `tests/test_migrate.py`, `tests/test_runner.py`,
   `scripts/migrate_to_central.py`. Under default filters it degrades to a single pytest warning
   (suite passed, 1 warning), but **`-W error::DeprecationWarning` / `PYTHONWARNINGS=error` breaks
   import**. Minibrisk for strict CI; recommend moving the warn inside `Central.__init__` or using
   `warnings.warn(..., stacklevel=2)` guard.
2. **Absolute path leak in prompt**: “Province-aware promotion destinations” block f-strings
   `province_*_dir()` (absolute) while step-8 verify block uses `.relative_to(REPO_ROOT)` (relative).
   Cosmetic/info-leak; recommend `.relative_to(REPO_ROOT)` for consistency.
3. **Test-count/coverage drift vs plan**: claimed “6 tests” for Task 1, actual 5; the
   plan-mandated overwrite-refusal test is missing (code path exists + raise FileExistsError
   — but not asserted), and PersonJSONFactory → classify is only empirically validated via E2E.

## Verdict: ✅ APPROVED

Phase 4 objectives are fully met and verified in code + live-run evidence: single-resolver routing,
province-aware dispatch prompt without legacy canonical block, province-first queue readiness with
task_id-based build candidates, two E2E artifact sets with clean FK checks, 243/243 regression, and
the commit set matches the plan. Findings above (R1–R3) are quality notes, not blockers; add the
overwrite-refusal unit test and path-format consistency in any follow-up cleanup.