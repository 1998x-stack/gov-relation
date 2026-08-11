# Phase 3 (Legacy Migration) — Adversarial Review

**Date:** 2026-08-11
**Reviewer:** SubAgentReview (adversarial, read-only)
**Scope:** Phase 3 Tasks 1–2 of `docs/superpowers/plans/2026-08-10-v3-phase3-5-migration.md`
(Phase 4/5: **not in scope** — excluded per tasking; checked as not starting, no Phase 4/5
commits exist in `git log` for this work except pre-existing plan checkboxes).
**Spec reference:** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md`

## Verdict: ✅ APPROVED

All Phase 3 gates verified end-to-end. No critical issues. 3 non-blocking findings
(all "uncommitted artifact / robustness" class — no source-logic defects found in scope).

---

## 1. Verification evidence

### 1.1 Git state (as expected)

```
$ git log --oneline -15
36562876e docs(migrate): record holdout triage decision (test/placeholder, stay excluded)
1f01bd5da docs(plan): mark Phase 3 tasks complete
bd3d9e615 refactor(web,inventory): scan both legacy and province paths
622f46493 feat(migrate): add legacy-to-provinces migration with --dry-run
... (Phase 1/2 commits below)
```

- `622f46493` = script + `data/migrations/province_artifact_map.json` + `unresolved_holdout.json` ✓
- `bd3d9e615` = `gov_relation/web.py` + `gov_relation/inventory.py` only ✓
- Uncommitted working-tree items present (other lanes) as noted; repo not modified by this review.

### 1.2 Task 1 — migration script (`scripts/migrate/migrate_legacy_to_provinces.py`)

Read in full. Reviewed mechanisms:

- **Person overrides + filename fallback:** override consulted first (`if relative in overrides`),
  slug validated against `PROVINCE_SLUGS.values()` → invalid override lands in `unmatched`
  (`invalid-override:<slug>`), never mis-migrates. Filename fallback then tries (a) 8-char
  prefix → `parts[1:]`, (b) else `parts[3:]`, scanning remaining segments for a segment ∈
  `PROVINCE_SLUGS`. **Deviation from the plan's reference implementation:** committed code has
  no `isdigit()` check and unconditionally drops 3 segments for any non-8-char first segment;
  the plan's version keeps all segments when no date prefix exists. A no-date-prefix file
  (e.g. `四川省-成都市-…-张三.json`) resolves under the plan's code but not the committed code.
  Direction is fail-safe (→ `unmatched`, never wrong destination). Currently masked: `unmatched=[]`
  because all non-conforming files (14) are covered by overrides. Recommend adopting the plan's
  defensive branch (minor).
- **Holdout consumption:** `load_holdouts()` reads `unresolved_holdout.json` → `artifacts[].path`;
  held files are counted in `stats["holdout"]` and excluded from gates. ✓
- **PROVINCE_SLUGS validation:** override slugs invalid if not in `PROVINCE_SLUGS.values()`
  (db/graph branch) or `PROVINCE_SLUGS.values()` (person branch). `_province_name()` reverse-lookup
  matches the F3-#5 fix (dir functions take Chinese province name). All 305 map values valid
  (`invalid slugs: 0`). ✓
- **Override paths verified on disk:** 0 missing of 305; 0 missing of 4 holdout paths. ✓
- **Idempotence guard:** `_link()` refuses to replace an existing non-hardlink destination
  (`FileExistsError`); inode-equal destinations report `existing-hardlink`. ✓

### 1.3 Dry-run (exact numbers)

```
$ python3 scripts/migrate/migrate_legacy_to_provinces.py --dry-run   (exit 0)
databases: 2290   graphs: 2281   persons: 6629
holdout:   4   ['data/database/openping_network.db',
                'data/database/test_region_network.db',
                'data/graph/test_region_network.gexf',
                'data/persons/20260723-test.json']
unmatched: []   ambiguous: []
actions: 11200, all status 'existing-hardlink'
```

- 2290 + 2281 + 6629 = **11,200** migrated artifacts; +2 db +1 gexf +1 person = 11,204 on-disk
  (on-disk count: db 2292, gexf 2282, persons 6630 — matches exactly; the 4 holdouts are the only
  exclusions, so `unmatched=0, ambiguous=0` claim is internally consistent).
- **Cross-check vs map file:** audit ledger claims "261 unmatched + 48 ambiguous → 305 overrides
  + 4 holdouts" (309 = 305+4 ✓). Map = 150 db / 141 gexf / 14 persons = 305 ✓.
- Provisional: all 11,200 statuses `existing-hardlink` ⇒ real re-run safe per idempotence rule.

### 1.4 Real re-run (idempotence, performed since dry-run showed 100% existing-hardlink)

```
python3 scripts/migrate/migrate_legacy_to_provinces.py   → exit 0
databases=2290 graphs=2281 persons=6629 holdout=4 unmatched=[] ambiguous=[]
statuses: Counter({'existing-hardlink': 11200})   # ZERO new links
```
No `FileExistsError`, no state change. Idempotent as claimed.

### 1.5 Mapping file spot-checks (`data/migrations/province_artifact_map.json`)

```
type dict, len 305, Counter({'db': 150, 'gexf': 141, 'persons': 14})
invalid slugs: 0
```
Spot-checked (inode equality source ⇄ destination):
- `data/database/aksai_network.db` → `data/provinces/gansu/database/…` hardlink=True
- `data/database/anyi_network.db` → `jiangxi/database` hardlink=True
- `data/graph/aksai_network.gexf` → `gansu/graph` hardlink=True
- `data/graph/anyi_network.gexf` → `jiangxi/graph` hardlink=True
- `data/persons/20260716-beijing-dongcheng-sunxinjun.json` → `beijing/persons` hardlink=True
- `data/persons/20260716-永泰-福州-代县长-林吓清.json` → `fujian/persons` hardlink=True

The 14 person overrides are exactly the filenames whose segments contain no province name
(e.g. `永泰-福州-…`, `河北省张家口市赤城县-…`) — the "filename province-segment fails" class
the plan describes. ✓

### 1.6 Holdout file (`data/migrations/unresolved_holdout.json`)

`status=triaged`, `decision=test/placeholder — excluded from migration (user-approved 2026-08-11)`,
4 artifacts with per-artifact `reason` + `resolution`. Cross-checked against real files:
- `openping_network.db` — **0 bytes** on disk ✓ (matches "0-byte stub")
- `test_region_network.db` / `.gexf` — test fixtures ✓
- `20260723-test.json` — stub person 张三, no birthplace/organization ✓

### 1.7 Tests

```
python3 -m pytest tests/test_legacy_province_migration.py tests/test_migrate.py -q
→ 8 passed, 1 warning (central DeprecationWarning)

python3 -m pytest tests/ -q
→ 241 passed, 1 warning
```

`test_legacy_province_migration.py` covers the resolution invariants (unique / ambiguous /
override-wins). `test_partitioned_inventory.py` covers hardlink dedupe, cross-province same-name
retention, province report visibility, province-path preference — matching plan Task 2 Step 2's
promised tests.

### Task 2 — web/inventory scan provinces (commit bd3d9e615)

- `gov_relation/web.py`: `_partitioned_files()` scans `PROVINCES_DIR/<p>/<subdir>` first then
  legacy, dedupes by `(st_dev, st_ino)` (hardlinks suppressed, non-link copies kept), returns
  `province_slug` on every row. `list_databases/list_graphs/list_person_profiles/list_reports`
  all use it. Province preferred over legacy for hardlink pairs ✓
- `gov_relation/inventory.py`: `_partitioned_paths()` same inode dedupe; orphan comparison uses
  `(province, stem)` tuples (cross-province same-name regions no longer cancel) ✓
- Behavior:
  - `list_databases()` → **2294** DBs = 2292 legacy inodes + 2 province-only v3 DBs
    (南丹县/大化瑶族自治县); the 2290 migrated DBs are hardlinks sharing legacy inodes → not
    double-counted; exactly 2 legacy-only entries (the 2 holdout DBs) ✓
  - graphs 2284, persons 6634, reports 1458 (web) / 1459 (inventory `*` pattern) — consistent
  - `scripts/inventory.py`: Databases 2294, GEXF 2284, Person JSON 6634, Reports 1459 ✓
  - `scripts/govdb.py audit`: schema_version 3.0.0, foreign_key_errors=[] ✓ (final-validation gate)

---

## Findings

None blocking. Ranked:

1. **[Moderate] Phase 3 test files are untracked.** `tests/test_legacy_province_migration.py`
   and `tests/test_partitioned_inventory.py` are `??` in `git status`; neither `622f46493` nor
   `bd3d9e615` includes them. The "241 passed" claim (plan completion record) depends on files
   not in git — a fresh checkout would run without them and the count would drop (and the
   migration/inventory behavior they pin would be unguarded). Plan Task 2 Step 2 explicitly
   promised these tests. Recommend committing them with the feature (not done in this review
   — read-only).
2. **[Moderate, adjacent scope] `data/provinces/` is entirely untracked** (0 tracked files, not
   gitignored; 11,338 files incl. 11,200 hardlinks + 138 non-hardlink entries: 124 `.gitkeep` +
   14 v3 originals for guangxi 南丹县/大化瑶族自治县 and heilongjiang reports). Hardlinks are
   fully reproducible from committed legacy + map file (proven by idempotent re-run), but the
   138 originals would be lost on clean checkout. Committing is Phase 4 Step 5's job (out of
   scope); flag for cross-lane coordination.
3. **[Minor] Committed person-filename fallback deviates from the plan's reference code** (no
   `isdigit()`/length guards; unconditionally strips 3 segments for any non-8-char prefix;
   plan keeps full parts). Fail-safe (unmatched, never wrong link); zero impact on current
   corpus (verified `unmatched=[]`); recommend syncing to plan's defensive branch.

Also noted (required by tasking, not actionable here — do NOT clean):
- `docs/assets/*.json` (10 files) + `docs/index.html` regenerated, uncommitted (expected).
- `data/provinces/` untracked (see finding 2), `scripts/migrate/upgrade_schema_v2_to_v3.py`
  untracked (Phase 2 lane), `data/migrations/external_data_merge_20260811.json` untracked
  (spec §10 external-merge output; no plan step covers it — suggest a future housekeeping commit).

## Plan checklist reconciliation (Phase 3 section)

| Plan step | State | Evidence |
|---|---|---|
| T1 S1 implement script | **Done** | `622f46493`, script read & exercised |
| T1 S2 dry-run test | **Done** | exit 0; 2290/2281/6629 + holdout 4, unmatched/ambiguous empty |
| T1 S3 execute migration | **Done** | real re-run exit 0, all 11,200 `existing-hardlink`, no new links; gate enforced (unresolved ⇒ exit 2) |
| T1 S4 commit | **Done** | `622f46493` (script + 2 json) |
| T2 S1 web.py scan | **Done** | `bd3d9e615`, all 4 list_* via `_partitioned_files`, `province_slug` present, inode dedup |
| T2 S2 inventory.py | **Done** | `bd3d9e615`; new tests exist but **uncommitted** — Finding 1 |
| T2 S3 verify | **Done** | 241 passed; list_databases=2294 containing legacy+provinces |
| T2 S4 commit | **Done** | `bd3d9e615` (code only; tests missing — Finding 1) |
| Phase 4 Tasks, Phase 5 Tasks, 全量最终验证 | **Out of scope** (not reviewed; Phase 4/5 not started — checkboxes left as-is) | — |

No step in the Phase 3 section remains **missing**. Nothing in Phase 3 is **obsolete**.

---

**Verdict: APPROVED.** Critical issues: none. Top 3 findings: (1) uncommitted Phase 3 tests —
claim "241 passed" is not reproducible from git; (2) `data/provinces/` fully untracked, incl.
138 v3 originals at risk (Phase 4 commit pending); (3) person filename fallback is less
defensive than the plan's documented code (fail-safe, currently masked).