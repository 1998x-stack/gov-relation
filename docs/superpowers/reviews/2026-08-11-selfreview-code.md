# Self-Review: 2026-08-11 Code Fixes (adversarial)

Date: 2026-08-11 · Reviewer: adversarial self-review subagent · Scope: today's 8 fix groups · Read-only (no edits, no commits, no destructive git)

## Global verification

```
$ python3 -m pytest tests/ -q
244 passed, 12 warnings in 2.53s        # expected 244 ✓ (12 warnings incl. Central deprecation warn, non-fatal)

$ python3 scripts/migrate/migrate_legacy_to_provinces.py --dry-run > /tmp/dryrun.json
databases=2290, graphs=2281, persons=6629, holdout=4 (openping_network.db / test_region_network.db / test_region_network.gexf / 20260723-test.json), unmatched=[], ambiguous=[]
→ migration gate intact ✓
```

All fix files match HEAD (no uncommitted drift in `build_factory.py`, `dispatch.py`, `central.py`, migrate script, or the 4 test files).

---

## F1 — F4 repo-root location (`276320464`) — **PASS** (one stale doc, see F7)

Evidence:
- `gov_relation/factory/build_factory.py` emits `_repo_root()` that walks `Path(__file__).resolve().parents` looking for a dir containing `gov_relation/`, raising `RuntimeError` if not found; `REPO_ROOT = _repo_root()`. No `parents[2]` anywhere in the template.
- Correct at **scripts/build/ depth** (parents: build → scripts → root; finds `gov_relation/`). Also correct at deeper depths — notably `region_factory.generate_build_script()` writes generated scripts to `data/provinces/<slug>/build/` (4 levels deep), where the old `parents[2]` would resolve to `data/provinces` and break execution. The fix is therefore *required*, not cosmetic.
- `tests/test_factory/test_build_factory.py` still meaningful: creates a `gov_relation/` marker dir in `tmp_path`, executes the generated script end-to-end (DB+positions+relationships+person JSON+report asserted), plus string-level guards `'def _repo_root()' in script` and `'Path(__file__).resolve().parents[2]' not in script`.
  - Caveat (minor): at the test's layout depth (`tmp/scripts/build/x.py`), `parents[2]` == the marker dir too, so the *execution* would pass under either scheme; the discriminating power is the string assertion. No test executes a generated script from the deeper province-build dir — the one depth the fix actually unlocks. Low risk, could add later.
- No test anywhere asserts old behavior.

## F2 — Person filename parse guards (`bf4c9ee54`) — PASS

- `scripts/migrate/migrate_legacy_to_provinces.py` now:
  `len(parts)>=2 and len(parts[0])==8 and parts[0].isdigit()` → drop 1 seg; `elif len(parts)>=4 and len(parts[0])==4 and parts[0].isdigit()` → drop 3; else keep all. Fail-safe (no unguarded unconditional drop).
  - Old code was `parts[1:] if parts and len(parts[0])==8 else parts[3:]` — the else branch dropped 3 segments unconditionally, e.g. `"安阳市-市委书记-李明"` → `[]` (province silently lost). New code keeps all → correct. Demonstrated side-by-side (see appendix).
- Dry-run numbers unchanged and exact: 2290 / 2281 / 6629 / holdout=4 / unmatched=[] / ambiguous=[].
- No test asserts old behavior: `tests/test_legacy_province_migration.py` only tests `resolve_province()` semantics (unique / ambiguous / override).

## F3 — Gold views tests (`276320464`) — PASS

- `tests/test_factory/test_gold_views.py` genuinely exercises implemented semantics:
  - test 1: seeds 1 current + 1 former position, asserts view returns only the current one (`is_current=1`, right person/org/title/start, `end_text=''`).
  - test 2: inserts a position with no organization_id, asserts `organization_name IS NULL` → proves the `LEFT JOIN organizations` branch.
- Implemented DDL in `schema_factory.py` matches: `FROM positions ps JOIN persons p … LEFT JOIN organizations o … WHERE ps.is_current=1`, selects `ps.title, o.canonical_name, ps.rank, ps.start_text, ps.end_text, ps.confidence` — no `administrative_rank`, confirms §4.5 annotation.
- Sanity: `SchemaFactory().create_all` on empty DB produces all 6 gold views.
- Suite: 34 passed in `tests/test_factory/`.

## F4 — Dispatch relative paths (`3de837e73`) — PASS

- Appended "Province-aware promotion destinations" block now uses `province_*_dir(province).relative_to(REPO_ROOT)` (4 fields). Canonical paths at the top of the prompt were already relative.
- No absolute-path leak: generated a real prompt for 四川省/测试市 → `ABS PATHS IN PROMPT: NONE`; block renders `- database_dir: data/provinces/sichuan/database`, etc.
- `tests/test_dispatch.py::test_includes_province_aware_promotion_destinations` asserts relative `data/provinces/jiangxi/database` present and old "Canonical destination…" phrasing absent.

## F5 — Central lazy deprecation (`3de837e73`) — PASS

- `$ python3 -W error::DeprecationWarning -c "import gov_relation.central"` → clean import, no warning.
- `Central('x')` under `-W error` → `DeprecationWarning: gov_relation.central is deprecated; use gov_relation.factory.InsertFactory` (raised in `__init__`, stacklevel=2).
- Suites using Central still pass (244 green; `test_runner.py` shows the warning non-fatally).

## F6 — Overwrite-refusal test (`2e2385525` + `3de837e73`) — PASS with accuracy note

- `tests/test_process_tmp_province.py` now has 6 tests; `test_promote_refuses_overwrite` (added in `3de837e73`) sets up an existing destination and asserts `pytest.raises(FileExistsError, match="destination exists")`.
- `promote()` in `.agents/skills/china-gov-network/scripts/process_tmp.py:151` raises `FileExistsError("destination exists: …")` only when `destination.exists() and not overwrite`, before any copy — verified.
- **Accuracy note:** `git log -S "destination exists"` shows the raise was introduced in `c006ee5d0` ("Set up gov relation worker queue"), i.e. predates these commits. The "test fails before the fix" claim is not literally true — the fix added the *test*, not the behavior. The test is still a valid regression lock of the required overwrite-refusal behavior (and it passed against both old and new code).
- Plan's five required behaviors (phase3-5 plan Task 1) are all covered, spread across test files:
  1. known province routing → `test_known_task_routes_database_to_province`
  2. unknown task fallback → `test_unknown_task_keeps_legacy_destinations`
  3. dry-run does not write → `tests/test_process_tmp.py::test_dry_run_keeps_staging`
  4. PersonJSONFactory output classifiable → `tests/test_process_tmp.py` contract tests (`career_timeline`/`identity`/`source_register`)
  5. same-name destination refused → `test_promote_refuses_overwrite`
  Plus extras: todo-error propagation, checkpoint exclusion, WAL sidecar avoidance.

## F7 — Spec sync (`e4614908c`) — **FAIL for §9.2 accuracy** (see below)

- **§4.5 annotation: accurate.** DDL verified identical (positions + JOIN persons + LEFT JOIN orgs + `is_current=1` + start/end_text, no administrative_rank; `person_statuses` retained as entity table — present in `_TABLES` + index — and still referenced as fallback by `gexf_factory.py:25`). ✓
- **§11 annotation: accurate.** Phase 2 section formally deprecated, defers to phase2 plan Task 1; Phase 5 central removal note consistent with current deprecation-not-deletion state. ✓
- **§9.2 annotation: STALE/WRONG on two points** (spec line ~665): "已实现为 keyword-only `generate(*, slug, province_name, …)`**(另接受 `province_dir` 覆盖)**;生成脚本经 `run_build(..., backend="v3")` 执行,**并硬编码 `Path(__file__).resolve().parents[2]` 定位仓库根**".
  - No `province_dir` param exists anywhere in `BuildScriptFactory.generate` (grep of whole factory dir: only `region_factory` uses `province_dir()` internally).
  - Root location is `_repo_root()` (search parents for `gov_relation/`) since `276320464`; the "硬编码 parents[2]" claim was written in `e4614908c` (git-blame) *before* the F4 fix landed, and was never updated.
  - Top revision note claims "§4.5/§9.2/§11 已就地标注与落地实现的差异" — overbroad for §9.2.
  - Also note `docs/superpowers/reviews/2026-08-11-review-phase1-foundation.md` R6 (hardcoded-parents[2] description) is history and now stale; the optimization-plan doc (line 19) correctly records F4 as done. Only the spec §9.2 note is a *current* doc inaccuracy.

## F8 — Legacy archive (`fb1793c93`) — **ISSUE (incomplete commit)**

Verified good:
- `scripts/build/legacy/` has 435 files, all committed, byte-identical to the originals (automated `git diff fb1793c93^:<root> fb1793c93:<legacy>` across all 435 → no differences).
- Commit touched only `docs/SYSTEM_OVERVIEW.md` + the 435 legacy files (nothing swept).
- Working tree root: `find . -maxdepth 1 -name 'build_*.py'` → 0.

Problems:
1. **The 430 root deletions were never committed.** `git ls-files` (HEAD) still lists 430 root `build_*.py` (e.g. `build_七台河市_data.py`); `git status` shows 430 ` D` entries; only `git mv`'d 5 (ASCII-named) were staged as renames. `fb1793c93` staged only `scripts/build/legacy/`. So HEAD contains the full duplicate set at root + legacy/, and any fresh clone/checkout gets 880 build scripts with root ones resurrected. The archive is only half-persisted (plan record: "仅 5 个被 git 跟踪" is factually wrong — all 435 were tracked).
- Minor: `gov_relation/inventory.py:76` still scans `root.glob("build_*_data.py")` — now a dead scan (returns 0). Not broken, but a leftover "root path" reference in active code.
- One stale doc line: `docs/SYSTEM_OVERVIEW.md` row `| build_*_data.py | … 当前约 98 个 |` still lists root build scripts at top level and "根目录 build_*_data.py 数量" inventory bullet.
- Side effect (dormant): archived legacy scripts' internal `parents[2]`/`parents[1]` root logic is now off-by-one at its new depth (`legacy/` → parents[2]=scripts/build). They are archives, not executed by the pipeline, so acceptable — but any manual re-run of a legacy script would mis-locate the repo root.
- Stray: untracked root `s.py` ("Build 达孜区…", Jul-28) remains — not matched by `build_*_data.py` glob; harmless clutter, worth deleting.

## Final verdict

**CONDITIONAL PASS.** 7 of 8 fixes are correct and verified (F1–F6 PASS; F7 except doc §9.2; F8 except commit completeness). Two actionable items:

1. **Commit the 430 root deletions** (stage `git rm` for the root `build_*.py`) so HEAD matches the "root cleared" claim, then re-verify `git ls-files` root build count = 0. This is the only functional gap — duplicates exist in committed history.
2. **Fix spec §9.2 annotation** (line 665): drop the `province_dir` override claim and replace "硬编码 parents[2]" with `_repo_root()` (search up for `gov_relation/`), and soften/annotate the stale R6 statement in `2026-08-11-review-phase1-foundation.md` if it's meant to describe current state.

Optional cleanups: drop the dead `root.glob("build_*_data.py")` in inventory.py, update the two stale SYSTEM_OVERVIEW lines, remove `s.py`.

## Appendix — old vs new filename parse

```
20260806-吉林省-白城市-市委书记-李洪慈 | old: ['吉林省','白城市',…] | new: same
2026-08-06-河南省-安阳市-县委书记-李明东 | old: ['河南省','安阳市',…] | new: same
安阳市-市委书记-李明                  | old: []         | new: ['安阳市','市委书记','李明']   ← old dropped the province segment (bug)
20260806X-吉林-市长-王                 | old: ['王']     | new: ['20260806X','吉林','市长','王'] ← old dropped valid segments
```