# Self-Review: Repo Health & Reproducibility (2026-08-11)

**Scope:** Post-v3-refactor final state on `main` (HEAD `84e883b5c`), read-only.
**Method:** git inspection of the working repo + fresh local clone in `/tmp/selfreview-clone` + full pytest on the clean clone + targeted greps.
**Verdict: ISSUES** — the v3 feature work is committed and the code/test suite largely reproducible, but the **Phase 5 "archive" commit is only half-complete** (430 root scripts still tracked in HEAD, deletion uncommitted) and **188 of 435 archived entries are broken symlinks on a clean checkout**. Both must be fixed before the final state can be considered trustworthy.

---

## 1. Commit chain — mostly coherent, one anomaly

`git log --oneline -18` shows all expected commits in order. Per-commit verification:

| Commit | Expected content | Found |
|---|---|---|
| `276320464` Phase 1 | factory layer, paths/identity, 31-province skeletons, external merge | ✅ `gov_relation/factory/*.py` (8 factory modules), `identity.py`, `paths.py`, `runner.py` (242), `gov_relation/platform/{identity,importer,resolution}.py`, tests/test_factory/* (8 files), 124 `.gitkeep` (31 provinces × 4 dirs) + 2 new `scripts/build/build_guangxi_*.py`. 154 files, +3179. ⚠️ also adds junk to `.gitignore` (see §4) |
| `20ca249e9` Phase 2 | upgrade script + schema gate | ✅ `scripts/migrate/upgrade_schema_v2_to_v3.py` (182), `platform/schema.py` (+74), `scripts/govdb.py` (+45), `tests/test_schema_migration.py` (202), `tests/test_worker_gate.py` (156) |
| `bf4c9ee54` Phase 3 | regression tests + parse guards + web assets | ⚠️ Code part fine (`migrate_legacy_to_provinces.py` +7, 2 new tests, `process_tmp` harden), but **110,432 insertions / 60,096 deletions** of regenerated `docs/assets/data/*.json` (person_profiles.json ±96k lines). Plausibly a regen artifact, but the diff is enormous and was not independently reviewable here |
| `2e2385525` Phase 4a | process_tmp auto-route | ✅ `.agents/skills/china-gov-network/scripts/process_tmp.py` +44, new test (88) |
| `38a93c8df` Phase 4b | dispatch provides province paths + queue | ✅ `gov_relation/{dispatch,queue}.py` + tests |
| `8086baaa4` v3 chore | rights sync, central deprecation warn, sys.path | ✅ 5 files, small |
| `fb1793c93` Phase 5 archive | archive 435 root legacy scripts → `scripts/build/legacy/` | **❌ INCOMPLETE — see §1a** |
| `3de837e73` | review fixes | ✅ |
| `84e883b5c` | plan checkbox | ✅ |
| docs commits (`9e9d6ba7d`, `e6883c9b8`, `76f1e96e6`, `5a56f8248`, `1f01bd5da`, `2824bf131`, `36562876e`, `e4614908c`) | plan/review docs | ✅ all touch only docs |

### 1a. Phase 5 archive commit is only half-complete (MUST-FIX)

- `fb1793c93` only **adds** files under `scripts/build/legacy/` (435 files: 245 regular 100644 + 2 100755 + 188 symlinks 120000). It never deletes the originals.
- `git ls-files | grep -c '^"build_'` = **430 root-level `build_*.py` still tracked in HEAD**.
- Working tree deleted all 430 of them, **uncommitted**: `git status --short` shows 430 ` D` entries; `git diff --stat HEAD` = **443 files changed, 116,094 deletions**.
- Result: a fresh clone ships **both** 430 root originals **and** the 435-entry legacy archive (duplicated, ~100k lines). The archive commit message claims a state the commit does not contain. Fix: `git rm` the 430 root scripts in the archive commit (or revert the archive) and re-test.

### 1b. 188 of 435 archive entries are broken symlinks (MUST-FIX)

- Legacy dir contains 188 symlinks (mode 120000), e.g. `build_冷水江市_data.py` → target stored as `scripts/build/build_冷水江市_data.py`.
- Symlink targets are **repo-root-relative** but resolve **relative to the symlink's own directory** (`scripts/build/legacy/`), i.e. real path `scripts/build/legacy/scripts/build/build_...` — which exists in neither HEAD nor any worktree.
- Verified on BOTH main worktree and clean clone: `for f in scripts/build/legacy/*; do [ -L "$f" ] && [ ! -e "$f" ] && echo x; done | wc -l` → **188** in both. `readlink -f` fails; `ls scripts/build/legacy/scripts` → No such file.
- The target should have been `../build_..._data.py` (the targets ARE tracked at `scripts/build/` — verified `git cat-file -e HEAD:scripts/build/build_冷水江市_data.py` → yes).
- Net effect: 188 of the "archived" scripts are unreachable from the archive on any checkout; the only un-broken copy is the still-tracked root original.

---

## 3. Plan completion — Phase 2/3–5 clean; Phase 1 checklist NOT complete (ISSUE)

```
2026-08-10-v3-phase2-schema-upgrade.md: 0 unchecked   ✅
2026-08-10-v3-phase3-5-migration.md:   0 unchecked   ✅
2026-08-10-v3-phase1-foundation.md:   36 unchecked   ❌
```

`2026-08-10-v3-phase1-foundation.md` has **36 `- [ ]` items** remaining (e.g. lines 157/237/258/345/350/824/829/848/996/1001/1285/1291/1315/1408/1488/1493/1518/1621/1675/1849/1920/1925/1945/2102/2180/2185/2210/2216/2232/2263/2268/2279/2284/2301/2306/2326?) — i.e. most Task steps for Tasks 3–7 plus scattered "Step 5: Commit" items. Only 20 `- [x]` exist (mostly Task 1–3 steps and a review-fix section at the end). The claim "phase1 plan: zero unchecked" is **false**. The work itself is committed (`276320464` etc.), so this is doc/checklist debt, but it directly contradicts the "all checkboxes done" claim, and per-step verification records for Tasks 4–7 do not exist.

---

## 4. Clean-checkout reproducibility — tests: 239 passed / 5 failed (1 code bug + 4 runtime-data-dependent)

Fresh clone: `git clone -q . /tmp/selfreview-clone` → HEAD `84e883b5c-ish`, `git status` clean, 124 `.gitkeep`.

### 4a. Full suite on clean checkout

```
python3 -m pytest tests/ -q
→ 5 failed, 239 passed (244 collected), in 2.86s
```

| Test | Cause | Classification |
|---|---|---|
| `test_paths.py::test_repo_root_ends_with_gov_relation` | `assert REPO_ROOT.name == "gov-relation"` — hardcodes the checkout **directory name** | ✅ pure-code test bug: fails for any clone named differently (e.g. `mycheckout`) even with all data present |
| `test_process_tmp.py::TestProcessTmpCLI (3 tests)` | script loads `data/TODO.json` (gitignored runtime dispatch state) | 🔸 runtime-data-dependent: passes only in tree seeded with runtime files |
| `test_migrate.py::TestIntegration::test_slug_without_province_is_skipped` | `migrate_to_central.main()` → `FileNotFoundError: TODO.json not found at <clone>/data/TODO.json` | 🔸 same |

All 5 pass in the **seeded main worktree** (re-ran `tests/test_process_tmp.py` + the migrate test → 5 passed, 0.45s), confirming the split: 1 test-design bug (dirname assertion — trivial but real) and 4 tests that silently depend on an untracked runtime file. The repo-intent (runtime data out of git) is fine; the tests should expose fixtures/auto-skip markers, and `test_paths` should not assert the folder name.

### 4b. Import smoke

```
python3 -c "import gov_relation, gov_relation.factory.region_factory, gov_relation.dispatch, gov_relation.queue"
→ IMPORT SMOKE OK
```

### 4c. Skeleton (.gitkeep) policy — ✅

- Tracked `.gitkeep` in `data/provinces/`: **124** (= 31 provinces × 4 dirs `database/graph/persons/reports`), no non-`.gitkeep` files tracked under `data/provinces/`.
- On-disk (main): `find data/provinces -name .gitkeep` = 124, 31 dirs — matches policy.
- `git check-ignore data/provinces/anhui/database/foo.sqlite` → ignored ✅; `.gitkeep` → NOT ignored ✅ (negative rules working).
- Full clone was 2.4s; `.agents/skills/china-gov-network` tracked (9 files) so process_tmp tests can even run in clone.

**What a new developer sees:** clean tree; suite mostly green (239) with 5 fails; 4 of the fails stem from a missing `data/TODO.json` (runtime; the repo intentionally excludes it — but then these tests are mis-designed for a fresh checkout) + 1 directory-name assertion. Plus the doubled 430 root legacy scripts and 188 dangling symlinks described in §1a–1b.

---

## 5. Working-tree hygiene — NOT clean; v3/cleanup leftovers are still dirty (ISSUE)

`git status --short` (1041 lines):

- **430 ` D` root `build_*.py`** — the uncommitted half of the Phase 5 archive (§1a).
- **598 `??` untracked**: 597 are `docs/reports/*.html` (runtime report outputs — known/benign)… including **`docs/superpowers/reviews/2026-08-11-review-phase4.md` (untracked review doc!)** — should have been committed with the Phase 4 review.
- **12 tracked `M`**: `data/central/provincial/test_runner_prov.db` (runtime db, known) + 6 `docs/reports/*.html` & `report/open_gaps.md` (runtime) + **5 `scripts/build/build_{xinyu,乾县,兴安区,定边县,武功县}_data.py`** — uncommitted quote-style/docstring cleanup edits (e.g. curly quote → straight, removing `from __future__ import annotations`, a stray `"""`). Not v3-work, but uncommitted edits on tracked build scripts alongside a "everything merged" narrative.
- `.gitignore`: `data/provinces/**` + `!dirs` + `!.gitkeep` is correct; but lines 23–25 contain junk **`Added:` / `Last` / `Registry`** (committed long ago via `5e5e233e` context — actually pre-existing since `git log -S'Registry'` → `5e5e233`), harmless but junk.

So the claim "only docs/reports outputs, data DBs, a few build/data files remain dirty" is **partially wrong**: the 430 deletions and the 5 build-script edits are v3-cleanup-related uncommitted churn, and the phase4 review doc is untracked.

---

## 6. Stale docs — mostly synced; 3 stale items remain

- `ADDITIVE_SCHEMA_UPGRADES` misinformation — ✅ handled: spec strikethrough + 审查同步 note (spec lines 869/873 disagree with nothing) match plan Task 1 (empty set).
- `parents[2]` — **one stale spec note**: `specs/2026-08-10-v3-refactor-design.md` line 665 (2026-08-11 审查同步) still claims generated scripts „硬编码 `Path(__file__).resolve().parents[2]` 定位仓库根“; actual code `gov_relation/factory/build_factory.py` uses `_repo_root()` (walks parents for `gov_relation/` marker) — the R6 fix landed in `276320464`. Spec contradicts code. (`scripts/tools/generate_build_template.py` legitimately uses parents[2] — it lives at exactly that depth; not stale. Plan docs' parents[2] occurrences are in legacy-script context, fine.)
- Stale counts: `phase3-5-migration.md` line 302 says „241 tests passed", line 507 `[x] → 220 passed" — both dated; actual now 244 collected (239+5 in clean / 244 in seeded). `phase1-foundation.md` line 2329 correctly notes the 222→241 fix. 
- `test_paths` hardcoded dirname (see §4a) is arguably a docs/code-naming assumption as well.

---

## Verdict: **ISSUES** — must-fix list

1. **(High) Finish the Phase 5 archive move in git**: commit the removal of the 430 root `build_*.py` (currently 116k-line uncommitted deletions; HEAD still ships duplicates). 
2. **(High) Repair the 188 broken symlinks** in `scripts/build/legacy/` (retarget to `../build_...`. or materialize real copies) so the archive is browsable from a clean checkout.
3. **(Med) Phase 1 plan checklist debt**: mark off the 36 remaining `- [ ]` steps (with per-step commit refs as was done for Tasks 1–3) so "zero unchecked" is actually true.
4. **(Med) Clean-checkout tests**: (a) `test_paths` should assert on `REPO_ROOT.name` via `gov-relation` *or* any name — drop the literal-dirname assertion or derive from git remote; (b) decide the `data/TODO.json` dependency: seed a fixture or `skipif` when the runtime file is absent, else the suite is red on every fresh clone.
5. **(Low)** Commit or delete `docs/superpowers/reviews/2026-08-11-review-phase4.md`; decide on the 5 quote-cleanup edits in `scripts/build`; remove `.gitignore` junk lines “Added / Last / Registry”; refresh "224/241 passed" counts; fix spec line 665's stale `parents[2]` description.