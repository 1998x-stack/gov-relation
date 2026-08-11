# Review — Phase 1 (Foundation): Factory Implementation

- **Date:** 2026-08-11
- **Reviewer:** SubAgentReview (adversarial, independent)
- **Plan:** `docs/superpowers/plans/2026-08-10-v3-phase1-foundation.md` (2329 lines; uncommitted amendments present in working tree)
- **Spec:** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md`
- **Mode:** read-only. No source files modified; no commits made; no destructive commands.

---

## 1. Scope & Commands / Evidence

All commands run with `cd /workspace/data/xieming/other-codes/gov-relation && …`.

| Check | Command | Result |
|---|---|---|
| Git log | `git log --oneline -30` | No `feat(factory)`/`test(factory)` commits in main; latest `36562876e docs(migrate): record holdout triage…` |
| Git status | `git status --short` | Phase-1 files: `?? gov_relation/factory/`, `?? gov_relation/identity.py`, `?? tests/test_factory/`, `?? data/provinces/`, `?? data/migrations/external_data_merge_20260811.json`, `M gov_relation/paths.py`, `M gov_relation/platform/identity.py`, `M gov_relation/gexf.py`, `M gov_relation/runner.py`, `M gov_relation/platform/importer.py`, `M gov_relation/platform/resolution.py`, `M scripts/govdb.py`, `M tests/test_platform.py`, `M tests/test_paths.py` (all uncommitted) |
| Worktrees | `git worktree list` | Second worktree `.claude/worktrees/v3-refactor` @ `a43b45022 [worktree-v3-refactor]` containing an **older, divergent** implementation (`refactor(identity)…`, `feat(paths)…`, `feat(factory): SchemaFactory with full v3 DDL…`); not an ancestor of main (`git merge-base --is-ancestor … → NO`) |
| Factory tests | `python3 -m pytest tests/test_factory/ -q` | **32 passed** in 0.84s |
| Full suite | `python3 -m pytest tests/ -q` | **241 passed**, 1 warning in 2.80s |
| Platform tests | `python3 -m pytest tests/test_platform.py -q` | 6 passed |
| Imports | `python3 -c "from gov_relation.factory import …; import gov_relation.factory.region_factory, …"` | All 7 classes + 7 submodules import cleanly; `stable_id('test','hello')` → `test_<hex>` |
| Inventory | `python3 scripts/inventory.py` | exit 0; repo-wide counts printed; 13 DB-without-GEXF / 6 GEXF-without-DB legacy inconsistencies (pre-existing, out of scope) |
| Province dirs | `python3 -c "…len([d for d in PROVINCES_DIR.iterdir() if d.is_dir()])"` | 31 dirs; `PROVINCES_DIR.exists()` True; 124 `.gitkeep` (4 subdirs × 31) |
| Merge evidence | `cat data/migrations/external_data_merge_20260811.json` | Untracked, 2516 B: schema_version 1, merged_at 2026-08-11, source_file_count 38, method "process_tmp validation plus semantic SQLite/GEXF conflict review", 2 promoted, 1 replaced, 7 retained-with-reasons (sha256 + rationale) |
| Promotion contract | `grep source_register/career_timeline/identity .agents/skills/china-gov-network/scripts/process_tmp.py` (line 70) | Contract = `"identity"`, `"career_timeline"`, `"source_register"` present; PersonJSONFactory emits all three (+ `current_status` extra) |

## 2. Findings — Phase 1 Completion Checklist (12 items)

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | `gov_relation/identity.py` promoted from platform/ | **PASS** | Exists (untracked), canonical impl: `stable_id` UUIDv5 (`uuid.uuid5(_NAMESPACE,…)` with namespace `99f1252f-…`), `normalize_text`, `person_key`, `organization_key`, `date_precision`, `sha256_bytes`. `platform/identity.py` is a thin re-export (`from gov_relation.identity import …` + `__all__`). All 4 planned import sites moved to `gov_relation.identity` (verified: `platform/importer.py:11`, `platform/resolution.py:10`, `scripts/govdb.py:17`, `tests/test_platform.py:9`); no remaining `platform.identity` imports. |
| 2 | `paths.py` PROVINCES_DIR + PROVINCE_SLUGS + 6 province_*() | **PASS** | `PROVINCES_DIR = DATA_DIR/"provinces"`, `PROVINCE_SLUGS` (31 entries incl. `inner_mongolia`, `shaanxi`, `xizang`, `xinjiang`), `province_dir/build/database/graph/persons/reports` all present; `province_build_dir` returns `REPO_ROOT/scripts/build` per uncommitted plan amendment. `tests/test_paths.py` has 3 new tests incl. subdirectory helpers (pass). |
| 3 | `schema_factory.py` — 21 tables + 6 views + 21 indexes DDL | **PASS** (with deviation, see §3-D2) | `SchemaFactory.create_all/entity/evidence/rights/meta/views/indexes`; test `test_create_all_builds_21_tables_and_v3_columns` asserts exactly 21 tables + v3 columns + `schema_version=3.0.0`; 6 view DDLs and 21 index DDLs counted in source (`grep -c`). DDL is **not** the plan's inline v3 DDL: it extracts `CREATE TABLE` statements from `gov_relation.platform.schema.DDL` and adds v3 columns via `_V3_COLUMNS`/`ALTER TABLE` (matches spec §9.1 "引用 schema.py (DDL 常量)"). |
| 4 | `insert_factory.py` — 8 upsert/insert/link methods incl. claim | **PASS** | 8 methods: `upsert_person`, `upsert_jurisdiction`, `upsert_organization`, `insert_position`, `insert_relationship`, `insert_source`, `insert_claim`, `link_evidence`. Deterministic id keys; native `ON CONFLICT … DO UPDATE` upsert for persons; claim uses `stable_id("clm", …)` with `value_json` and no double-encoding (3 dedicated tests). |
| 5 | `gexf_factory.py` — DB → GEXF XML | **PASS** | `build(conn, title)` + `write()`; node ids = full stable string ids `person:{pid}` / `organization:{oid}` (test asserts `f"person:{first}" in xml`); title, edge type/context/overlap_period attvalues present; Task 5 Step 0 gexf.py refactor confirmed: shared `_build_tree()` used by both `write()` and `to_string()` (`gexf.py:103,198,204`). |
| 6 | `person_factory.py` — DB → Person JSON | **PASS** | `build(conn, person_id)` raises on unknown id; emits `identity`, `career_timeline`, `source_register` (populated from `sources` joined through `evidence_links`), plus `current_status`; `test_person_profile_satisfies_promotion_contract` passes; contract verified against `process_tmp.py:70`. |
| 7 | `report_factory.py` — stats → Markdown | **PASS** | `build(slug, stats)` table + `build_from_conn` (COUNT per table); `test_report_uses_database_counts` passes. |
| 8 | `build_factory.py` — data lists → fully runnable .py script | **PASS** | `BuildScriptFactory.generate(*, slug, province_name, …)` (signature drift vs plan, see risk D4); generated script delegates to `gov_relation.runner.run_build(…, backend="v3")` per amended global constraint; test **executes** the generated script end-to-end (`runpy`), then asserts DB rows, person JSONs, report file (passes). |
| 9 | `region_factory.py` — unified entry | **PASS** | `RegionResearchFactory(province, region, level, targets)` + add_* collectors (incl. `add_claim`); `generate_build_script/gexf/person_profiles/report` all route through `province_*_dir()` helpers and `runner.run_build(backend="v3")` (atomic temp-file publish + `PRAGMA foreign_key_check` guard in `runner._run_v3_build`). Integration test `test_full_region_pipeline_with_positions_and_relationships` passes. |
| 10 | `tests/test_factory/` — ~25 unit + integration tests | **PASS** (actual: 32) | 32 test functions (schema 4, insert 15, gexf 2, build 2, person/report 2, region 1, v3_runner 6 — the last two files are additions beyond the plan). All pass. Plan/checklist claim "22/25" is stale. |
| 11 | `data/provinces/` — 31 province skeletons | **PASS** | 31 dirs × {database, graph, persons, reports} with `.gitkeep` (124 total, `build` subdir intentionally skipped per amended Step 1). Note: tree also contains 11,214 real artifacts / 158 MB (see risk D6). |
| 12 | External data merge (2026-08-11) with conflict review | **PASS** | `data/migrations/external_data_merge_20260811.json` (untracked) documents semantic review: 38 source files, 2 promoted, 1 replaced, 7 retained repo versions with per-file sha256 + rationale; consistent with plan Task 8 Step 2 (marked `[x]`). Merge/upgrade: the json itself is untracked. |
| 13 | Full suite passes (checklist claims "222 passed") | **PASS** (claim stale) | Actual: **241 passed** (includes untracked Phase 2/3 test files `test_schema_migration.py`, `test_legacy_province_migration.py`, `test_partitioned_inventory.py`, `test_process_tmp_province.py`). |

## 3. RECONCILE — 36 unchecked `- [ ]` lines (35 real steps + 1 tooling note at line 3)

Legend: **(a)** done despite unchecked (cite evidence); **(b)** genuinely missing; **(c)** obsolete/backlog (TDD red-phase or N/A).

| Plan step | Classification | Evidence / citation |
|---|---|---|
| T1 S5 Commit (L157) | **(b)** — missing | No commit exists; `gov_relation/identity.py` untracked, `platform/identity.py` modified (uncommitted). |
| T2 S3 Commit (L237) | **(b)** — missing | `paths.py` modified, uncommitted. |
| T3 S1 write tests (L258) | **(a)** done | `test_schema_factory.py` (4 tests), pass. |
| T3 S2 run-tests-confirm-fail (L345) | **(c)** obsolete | TDD red step; implementation exists → cannot be observed now, as expected. |
| T3 S3 implement (L350) | **(a)** done | `schema_factory.py` present; implementation deviates (see D3). |
| T3 S4 run pass (L824) | **(a)** done | 4/4 pass. |
| T3 S5 Commit (L829) | **(b)** missing | `gov_relation/factory/ … untracked. |
| T4 S1 write tests (L848) | **(a)** done | 15 insert tests (incl. source-pk rejection, position tenure, claim encoding), pass. |
| T4 S2 run-fail (L1001) | **(c)** obsolete | TDD red step. |
| T4 S3 implement (L1001) | **(a)** done | 8 methods incl. `insert_claim`; improved vs plan (native UPSERT, no per-call commit — runner commits). |
| T4 S4 run pass (L1285) | **(a)** done | 15/15 pass. |
| T4 S5 Commit (L1291) | **(d)** missing | — |
| T5 S0 gexf.py refactor (L1315) | **(a)** done | `_build_tree()` shared (gexf.py:103–196; write:198–202; to_string:204–207). |
| T5 S1 write tests (L1408) | **(a)** done | 2 gexf tests (plan listed 3 — merged), pass; stable IDs asserted. |
| T5 S2 run pass (L1488) | **(a)** done | 2/2 pass. |
| T5 S5 Commit (L1493) | **(d)** missing | `gexf_factory.py` untracked; `gexf.py` modified-uncommitted. |
| T6 S1 PersonJSONFactory (L1518) | **(a)** done | + promotion-contract test. |
| T6 S2 ReportFactory (L1621) | **(a)** done | + test. |
| T6 S3 BuildScriptFactory (L1675) | **(a)** done, redesigned | see D4; executes via runner v3. |
| T6 S4 build tests (L1849) | **(a)** done | 2 tests incl. full runpy execution. |
| T6 S5 run (L1920) | **(a)** done | pass. |
| T6 S6 Commit (L1926) | **(d)** missing | — |
| T7 S1 region factory (L1945) | **(a)** done | incl. `add_claim` (plan didn't list it). |
| T7 S2 integration tests (L2102) | **(a)** done — 1 test (plan: 2) | `test_full_region_pipeline_with_positions_and_relationships`; empty-factory case not covered (minor gap). |
| T7 S3 run (L2180) | **(a)** done | pass. |
| T7 S4 exports (L2185) | **(a)** done | `__init__.py` exports all 7 classes. |
| T7 S5 all-factory run (L2210) | **(a)** done | 32 pass (plan: 22). |
| T7 S6 Commit (L2216) | **(d)** missing | — |
| T8 S1 create province dirs (L2232) | **(a)** done | 31 dirs, 4 subdirs each, 124 `.gitkeep`; step-1 shell loop unmatched by the `build`-skip only; matches plan. |
| T8 S3 verify count (L2263) | **(a)** done | 31 dirs printed. |
| T8 S4 Commit (L2268) | **(d)** missing | `data/provinces/` untracked. |
| T9 S1 full suite (L2279) | **(a)** done | **241 passed**. |
| T9 S2 import check (L2284) | **(a)** done | all imports OK. |
| T9 S3 inventory (L2301) | **(a)** done | exit 0. |
| T9 S4 final commit (L2306) | **(d)** N/A | verifying-only step; its premise "nothing to commit" is false — everything is still uncommitted. |

**Totals:** (a) = 24, (b/N-A) = 9, (c) = 2.

## 4. Deviations & Risks

- **R1 (CRITICAL) — No commits; entire Phase 1 exists only as working-tree state.** 9 plan Commit steps genuinely unexecuted. On `main`: `gov_relation/factory/`, `gov_relation/identity.py`, `tests/test_factory/`, `data/provinces/` are untracked; `paths.py`, `platform/identity.py`, `gexf.py`, `runner.py`, `platform/importer.py`, `platform/resolution.py`, `scripts/govdb.py`, `tests/test_platform.py`, `tests/test_paths.py` are modified-uncommitted. The required commit convention (`feat(factory): …` / `test(factory): …`) is unmet. A hard reset or cleanup would destroy the whole phase.
- **R2 (CRITICAL) — Duplicate/divergent implementation on second worktree.** `.claude/worktrees/v3-refactor` at `a43b45022 [worktree-v3-refactor]` contains an older schema_factory (standalone inline v3 DDL) + identity/paths that differ from the working tree versions. Two copies of Phase 1 exist; risk of committing the stale one or losing the current one. Need: commit working tree on main, then retire/supersede the old worktree branch.
- **R3 — SchemaFactory implementation strategy vs plan text.** Plan Task 3 specifies full inline v3 DDL in `schema_factory.py`; actual code reads/parses `gov_relation.platform.schema.DDL` and ALTERs in v3 columns. This matches spec §9.1 ("引用 schema.py (DDL 常量)") but makes `schema_factory` depend on `platform/schema.py` — which is itself **modified/uncommitted** (v3 columns `identity_status` CHECKs, `title_category`, `sort_order`, `commercial_use` etc. — verified present at platform/schema.py:125-189). If the platform schema edits are reverted or drift, Phase 1's DDL silently changes; `_table_statement()` hard-fails (`RuntimeError`) if a table is missing. Also `create_views()` executes `DROP VIEW IF EXISTS` first (plan only had `CREATE VIEW IF NOT EXISTS`) — it can clobber manually-customized views on existing DBs (by design, but worth flagging).
- **R4 — `gold_current_positions` view semantics differ from spec §4.5.** Spec: `FROM person_statuses ps … WHERE ps.is_current_confirmed=1`, selecting `post_text/org_text/admin_rank`. Implemented: `FROM positions ps … LEFT JOIN organizations … WHERE ps.is_current=1` (+ `start_text/end_text`). `person_statuses` is now essentially vestigial (only a fallback inside GEXFFactory); no test exercises `gold_current_positions`. Consumers (later API/web phases per spec §4.5 remark) may get different current-leadership rows than spec'd.
- **R5 — Interface drift vs plan/spec text (no doc update).** `BuildScriptFactory.generate()` is keyword-only `(slug, province_name, …)` — plan/spec §9.2 state `(slug, province_dir: Path, …)`. `link_evidence` returns `str` (spec: `-> None`) — superset, benign. `RegionResearchFactory` requires known province (raises on unknown). The plan file's task bodies still show the old shapes; only the goal line + checklist were amended. Doc/interface mismatch is itself drift.
- **R6 — `province_build_dir` and REPO_ROOT of generated script.** Plan F4 fix (search parents for `gov_relation/`) is not used; generated scripts hardcode `Path(__file__).resolve().parents[2]` (exactly scripts/build depth) and write to `REPO_ROOT/data/provinces/<slug>`. Tests operate fine (script at `tmp/scripts/build/…`), but the "location-agnostic" claim in the amended plan text no longer holds.
- **R7 — checklist numbers stale.** "25 tests" (actual 32 functions); "222 passed" (actual 241). Minor, but do-not-trust signals for later phases.
- **R8 — data payload size.** `data/provinces/` — beyond the 124 `.gitkeep`s — contains **11,214 files ≈ 158 MB** (cumulated DBs/GEXF/person JSON/report from ongoing province work, incl. the 2026-08-11 merge). Plan Task 8 Step 4's `git add data/provinces/` would commit the entire payload. Decide intent: skeleton-only (ignore artifacts) vs data checkpoint; the checklist text still says "31省目录骨架".
- **R9 — untracked/other-concurrency.** Working tree carries other concurrent uncommitted work (`dispatch.py`, `queue.py`, `central.py`, `inventory/web`, `.agent skills`, migration scripts, `docs/assets`); none conflicts with Phase-1 files, but a blame/audit on Phase-1 modules must be done before commit. `data/migrations/external_data_merge_20260811.json` itself is untracked — the merge evidence is not yet preserved in git.
- **R10 (minor)** — GEXF node id prefixes differ from plan sketch (`"person:"`/`"organization:"` vs `"per:"`/`"org:"`); harmless. `tests/test_region_factory.py` has 1 test (plan 2), the "empty pipeline" case is not covered at region level (covered indirectly by gexf empty test).

## 5. Verdict: **CHANGES-REQUESTED**

The implementation itself is functionally complete, well-tested (32/32 factory, 241/241 full), and satisfies all four hard global constraints (UUIDv5 ids; date_precision; source_pk rejection for birth-less persons at `insert_factory.upsert_person`; GEXF full-string node ids; promotion contract). Verification evidence is independent — I did not trust the checkboxes; everything was re-run.

**Critical issues (must fix before marking Phase 1 done):**
1. **Nothing is committed** — all 7 factories + `identity.py` + `tests/test_factory/` + `data/provinces/` are untracked; `paths.py`, `platform/identity.py`, `gexf.py`, `runner.py` etc. are modified-uncommitted. Execute the 9 pending Commit steps (convention `feat(factory):` / `test(factory):`).
2. **Two divergent copies exist** (main working tree vs `worktree-v3-refactor` branch a3b45022). Resolve to one source of truth (commit working tree on main; delete/retire the stale worktree branch) to avoid committing the old implementation.
3. **Reconcile spec/plan drift & data policy**: update spec §4.5/§9.2 and plan interfaces to the shipped implementation (view semantics, `generate()`/signature, build-dir policy, reporting) or revert code to match; decide and document whether `data/provinces` 158MB payload is skeleton-only or data checkpoint; un-ignore merge evidence JSON; note `platform/schema.py` dependency must be committed before/with schema_factory.