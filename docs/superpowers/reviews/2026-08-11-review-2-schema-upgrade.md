# Review 2: Phase 2 (v3 Schema Upgrade + govdb.py Switch)

- **Date:** 2026-08-11
- **Reviewer:** SubAgentReview (adversarial, code-verified, read-only)
- **Plan:** `docs/superpowers/plans/2026-08-10-v3-phase2-schema-upgrade.md`
- **Spec:** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md`
- **Scope:** Phase 2 Completion Checklist (plan ~line 365) — 6 checked items; Task 2 (govdb gate) + Task 3 (migration script); Task 1 (deprecated)
- **Env:** `python3` = 3.10.12 (spec says 3.11; code is stdlib-only and passed on 3.10), pytest 9.1.1
- **Verdict: CHANGES-REQUESTED** — implementation is functionally correct and fully verified, but the phase's deliverables are **entirely uncommitted** while the completion checklist claims done (both plan commit steps are genuinely missing), the real migration left no backup artifact, and the spec still contradicts the adopted design in two places.

---

## 1. Verified against code

### V1 — v3 DDL in `schema_factory.py`; legacy `schema.py` untouched; Task-1 approach actually removed

**PASS.**

- `gov_relation/factory/schema_factory.py` (207 lines, working tree) is the single v3 DDL provider: `SchemaFactory` builds 21 tables from the platform `DDL` (`from gov_relation.platform.schema import DDL as PLATFORM_DDL`), applies the 4 v3 delta column groups via `_V3_COLUMNS`, defines 6 gold views (`_VIEWS`) and 21 indexes (`_INDEXES`), and stamps `SCHEMA_VERSION = "3.0.0"` in `create_all()`.
- Legacy `gov_relation/schema.py` is untouched v1/v2 compatibility code: it contains only `CREATE_PERSONS` … `CREATE_REGISTRY` style constants and `insert_*` helpers. **No `V3_*` identifier exists anywhere** in `gov_relation/`, `scripts/`, or `tests/` (`grep -rn "V3_ENTITY_DDLS|V3_SCHEMA_DDLS|V3_JURISDICTIONS|V3_PERSONS"` → zero hits). The plan's "verification command is dead (ImportError)" claim is true.
- Note: `gov_relation/factory/` is **untracked** in this tree (see C1). A *different* 459-line `schema_factory.py` was committed to branch `worktree-v3-refactor` (a43b45022); the working tree's 207-line extraction-based version supersedes it but is not committed anywhere.

### V2 — `govdb.py` versioned gate: shape-check not stamp-check; `--replace` refused on non-v3; build does read-only shape verification

**PASS (code + tests + live behavior).**

- `scripts/govdb.py` lines 28–62: `_is_v3_database(path)` opens the destination **read-only** (`connect(path, read_only=True)`) and requires BOTH `schema_meta.schema_version == SCHEMA_VERSION ("3.0.0")` AND `has_v3_shape(conn)`. Any `sqlite3.Error` → `False`.
- `build_database()` lines 79–101: if destination exists and `_is_v3_database()` is false → `SystemExit` **even with `--replace`**, pointing at the migration script. If v3-shaped but no `--replace` → refuses (legacy). Build then writes to `<dest>.building` and calls `create_schema(conn)` — **platform gate + idempotent DDL, not `SchemaFactory.create_all`**. No v3 factory tables are created by build. `create_schema` is NOT called on the existing target (only the fresh `.building` file).
- `gov_relation/platform/schema.py`: `SCHEMA_VERSION = "3.0.0"`, `ADDITIVE_SCHEMA_UPGRADES = set()` (empty, per Task 3 Step 0), `REQUIRED_V3_COLUMNS` + `has_v3_shape()`. `create_schema()`: stamped-incompatible → `RuntimeError`; **unversioned non-empty DB without v3 shape → `RuntimeError` with migration hint**; empty DB → init; stamped 3.0.0 → legacy behavior kept (documented in plan's 门禁加固 as intentional).
- Adversarial checks that passed:
  - `test_worker_gate.py::test_build_refuses_*` × 3 (v2 stamp, missing stamp, false 3.0.0 stamp) all refuse with `--replace`, destination untouched.
  - A fresh fabricated v2-shaped DB **stamped 3.0.0** (= the "old create_schema stamped without ALTER" attack) is refused by `build_database` (shape check) and is correctly **repaired** by the migration script (not skipped) — 6 ALTERs, backfill, `has_v3_shape` → True.

### V3 — Migration script exists, runnable, isolated v2-fixture test

**PASS functionally; FAIL as committed artifact (untracked) — finding #1.**

- `scripts/migrate/upgrade_schema_v2_to_v3.py` (182 lines) exists, runs:
  - `python3 scripts/migrate/upgrade_schema_v2_to_v3.py --help` → usage, exit 0.
  - `--database data/platform/gov_relation.db --dry-run` → `{"status": "skipped", "reason": "already v3.0.0"}`, exit 0 (safe — dry-run mode `connect(..., read_only=True)`).
  - Real-run (on a throwaway copy) → `{"status": "upgraded", ...}` with exactly the 6 planned ALTERs, `.pre-v3.bak` backup created, second run → `skipped` (idempotent).
- Isolated v2-fixture tests: `tests/test_schema_migration.py` — 3 migration tests use `tmp_path` v2 DBs built by stripping v3-only columns from platform DDL: dry-run modifies nothing, missing DB raises, upgrade backfills (`title_category ← category` asserted as `'党委正职'`), idempotent, backup holds 2.1.0 stamp.
- **Findings:** the file is **untracked** (`?? scripts/migrate/upgrade_schema_v2_to_v3.py`) along with both gate test files; it is not in HEAD and not on `worktree-v3-refactor` either.

### E — Real migration done; FK audit errors = 0

**PASS (state verified); evidence gap on method (see issue #2).**

- Live DB `data/platform/gov_relation.db` (355 MB): `schema_version = 3.0.0`; all v3 columns present in `persons` (education, merged_into_id), `positions` (title_category, sort_order), `datasets`/`sources` (commercial_use); legacy columns retained (`positions.category`, `datasets/sources.commercial_use_allowed`); 21 tables + 7 gold views (incl. `gold_commercial_claims`) present.
- Backfill evidence: `positions.title_category` populated 12,147 rows == `positions.category` populated 12,147 (backfill ran); `datasets.commercial_use` 0 == `commercial_use_allowed` 0 (no cleared rights, consistent).
- `python3 scripts/govdb.py audit --database data/platform/gov_relation.db` → `"foreign_key_errors": []` (exit 0). **FK audit errors = 0 ✓** (plan claim holds).
- Evidence gap: no `data/platform/gov_relation.db.pre-v3.bak` exists (auto-backup would be created by the script on first real run per `upgrade()` line 96). DB mtime 03:24–03:25 vs code evolution — the real run either predates the backup logic or the backup was deleted. Cannot fully reconstruct; the resulting DB state is correct and consistent.

### Gate / test suites

**PASS — exact numbers match the plan claim.**

- `python3 -m pytest tests/ -q -k "gate or govdb or schema or upgrade"` → **40 passed, 201 selected** (0 failures).
- `python3 -m pytest tests/test_schema_migration.py tests/test_worker_gate.py tests/test_platform.py tests/test_schema.py -v` → **39 passed** (migration 10 = 3 migration + 7 create_schema gate; worker_gate 5; platform 6; schema 18).
- **Gate tests count = 7 + 5 = 12** exactly as the plan's "新增门禁测试 12 例".
- Full suite `python3 -m pytest tests/ -q` → **241 passed, 1 warning — matches "241 passed" exactly.**
- Migration script runnability proven via `--help` + dry-run + 3 isolated tests (no re-migration of the real DB performed; dry-run was the safe-mode check and returned `skipped`).

### D5 — Deprecation coherence (Task #1 废弃)

**PASS.** The plan's Task #1 note is coherent: no `V3_ENTITY_DDLS`/`V3_SCHEMA_DDLS` anywhere (`grep` empty); nothing imports them; `gov_relation/schema.py` remains v1/v2-only. The plan's adopted architecture (factory as single DDL provider + platform `create_schema` gate) is exactly what the code implements. Residual: **the spec is stale — 2 contradictions** (issue #3).

---

## 2. Reconcile every `- [ ]` step (~9)

| Step | Reality | Status |
|---|---|---|
| Task 2 Step 1 — gate in `build_database` (create_schema, not factory) | `scripts/govdb.py` lines 79–103 | **done-but-unchecked** ✓ |
| Task 2 Step 2 — `pytest tests/test_platform.py` | 6/6 passed (also green in full suite) | **done-but-unchecked** ✓ |
| Task 2 Step 3 — commit `scripts/govdb.py` | `M scripts/govdb.py` in working tree; **no commit contains it**; `worktree-v3-refactor`'s govdb.py is pre-gate (no `has_v3_shape`, imports old identity) | **genuinely missing** ✗ |
| Task 3 Step 0 — platform/schema.py version tolerance (3.0.0, empty ADDITIVE, 4 delta groups in DDL) | Verified in code | **done-but-unchecked** ✓ |
| Task 3 Step 1 — implement migration script | Exists, runnable, tested | **done-but-unchecked** ✓ *(file untracked)* |
| Task 3 Step 2 — dry-run on real v2 DB | Cannot reproduce (DB already v3 → dry-run returns `skipped`); dry-run verified on v2 fixture instead | **done (indirect evidence)** ⚠️ |
| Task 3 Step 2b — verify on copy | No artifact survives; final state consistent | **done (indirect)** ⚠️ |
| Task 3 Step 3 — real execution (upgraded → skipped on 2nd run) | DB stamped 3.0.0, v3-shaped, FK 0; re-run → `skipped` | **done-but-unchecked** ✓ |
| Task 3 Step 4 — commit** script + platform/schema.py | Both uncommitted (`??` + `M`) | **genuinely missing** ✗ |

→ 7 done-but-unchecked, 2 genuinely missing (both commit steps), 0 obsolete. **No stale "did it" box — but the two missing commits contradict the checked completion list (which asserts the phase is complete), and the phase's core artifacts are under-committed.**

---

## 3. Critical issues

1. **CRITICAL: entire Phase 2 is uncommitted while the checklist is marked `[x]` complete.** Untracked: `scripts/migrate/upgrade_schema_v2_to_v3.py`, `tests/test_schema_migration.py`, `tests/test_worker_gate.py`, `gov_relation/factory/`. Modified-uncommitted: `scripts/govdb.py`, `gov_relation/platform/schema.py`. Task 2 Step 3 and Task 3 Step 4 ("Commit") are still `- [ ]` and nothing in `git log` (HEAD, nor branch `worktree-v3-refactor`) carries any Phase-2 change — the branch only has Phase-1 commits and its `govdb.py`/`platform/schema.py` are pre-Phase-2 (SCHEMA_VERSION 2.1.0, ADDITIVE includes 2.0.0/2.1.0-era, no `_is_v3_database`). A phase claimed complete is one crash/`git clean -fd` away from total loss.

2. **Real migration executed without surviving backup artifact.** The script's real path auto-creates `<db>.pre-v3.bak` (line 96); none exists at `data/platform/`. Plan requires "执行前务必备份…先在副本验证" — cannot be confirmed post hoc (either backup was deleted or migration predates the backup code). DB state itself is correct (stamp, shape, FK 0, backfill consistent), so this is evidence/auditability, not data risk. (This may also explain why the plan-mandated `.pre-v3.bak` is missing: the canonical run predates the final script — an indication the script evolved after the real migration.)

3. **Spec contradicts the adopted plan/implementation in two places.** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md` §11 Phase 2 still says: «`gov_relation/schema.py` 升级到 v3 DDL（保留 v2 legacy 常量）» and «同步升…`ADDITIVE_SCHEMA_UPGRADES` 纳入 2.1.0». The adopted plan and the code do exactly the opposite (factory holds v3 DDL; `ADDITIVE_SCHEMA_UPGRADES = set()` — adding 2.1.0 there would be the "fake upgrade" the plan explicitly forbids). Anyone reading the spec for Phase 2/3 will be misled. The plan's deprecation note is coherent; the spec was never updated.

Minor notes (non-blocking):
- `upgrade()` parameter is loosely typed (a plain `str` raises `AttributeError` on `.with_suffix`); argparse passes `Path`, tests pass `Path` — cosmetic, not a defect. The plan sketch's `"(dry) "` prefixes differ from the final script's labels — matches the delivered behavior and dry-run test.
- Environment runs Python 3.10.12 (plan says 3.11); stdlib-only verified — no 3.11-specific dependencies, full suite green on 3.11-compatible stdlib surface.
- `test_schema_migration.py::test_create_schema_keeps_legacy_behavior_for_stamped_v3_without_shape` deliberately encodes that a false-stamped 3.0.0 DB is accepted by `create_schema` (legacy behavior retained per plan). The build gate closes this hole; document it (or decide to shape-check stamped DBs in a later phase).

---

## 4. Evidence trail (commands, all read-only)

- `git status --short` → `?? scripts/migrate/upgrade_schema_v2_to_v3.py`, `?? tests/test_schema_migration.py`, `?? tests/test_worker_gate.py`, `?? gov_relation/factory/`, `M scripts/govdb.py`, `M gov_relation/platform/schema.py`, `M docs/.../phase2-plan.md` (+ unrelated concurrent work)
- `git log --oneline -30` → no Phase-2 commits; `worktree-v3-refactor` branch contains only Phase-1 commits (a43b45022 etc.), its govdb.py/schema.py are pre-Phase-2
- `python3 -m pytest tests/ -q` → 241 passed (1 warning)
- `pytest -k "gate|govdb|schema|upgrade"` → 40 passed
- `pytest test_schema_migration.py test_worker_gate.py test_platform.py test_schema.py` → 39 passed
- `upgrade_schema_v2_to_v3.py --help` → exit 0; `--dry-run` on real DB → skipped/already v3.0.0, exit 0
- Live DB: stamp 3.0.0; PRAGMA columns all v3-present; `govdb.py audit` → `foreign_key_errors: []`
- Adversarial: fake-stamped v2-shaped DB → migration reports 6 ALTERs + backup + shape True; `build_database` refuses (v2/false-stamped/unstamped) even with `--replace`

---

**Verdict: CHANGES-REQUESTED** — proceed with the phase only after: (1) committing the Phase-2 artifacts (migration script/tests, `govdb.py`, `platform/schema.py`, factory) and checking Tasks 2 Step 3 / 3 Step 4; (2) confirming the real-migration backup trail (or documenting why none exists); (3) updating the two spec contradictions (or marking the old Phase-2 spec block deprecated like the plan's Task #1).