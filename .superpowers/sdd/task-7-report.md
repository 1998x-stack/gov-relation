# Task 7 Report: Migration script

**Status:** DONE

**Commit:** `7c7cab5d` — `feat: one-time migration script from region DBs to central registry`

## Files changed

| File | Change |
|------|--------|
| `scripts/migrate_to_central.py` | **Rewritten** — complete one-shot migration script (238 lines). Reads every `data/database/*_network.db`, rekeys foreign keys via content hashes, writes into province-partitioned central DBs. Supports `--dry-run`, `--limit`, `--resume`, `--province` flags. |
| `tests/test_migrate.py` | **Created** — 5 integration tests verifying migration logic against a fake legacy-format DB |

## Verification

### Unit tests (5/5 pass)

```
tests/test_migrate.py::TestMigrateOne::test_migrate_populates_central        PASSED
tests/test_migrate.py::TestMigrateOne::test_migrate_minimal_db               PASSED
tests/test_migrate.py::TestMigrateOne::test_migrate_no_relationships         PASSED
tests/test_migrate.py::TestMigrateOne::test_migrate_person_without_name      PASSED
tests/test_migrate.py::TestIntegration::test_slug_without_province_is_skipped PASSED
```

### Full test suite (162/162 passed)

```
162 passed in 0.97s
```

### Dry-run integration test

```
$ python3 scripts/migrate_to_central.py --dry-run
→ 229 DBs can be mapped (out of 1668 total)
→ The rest (~1439) have slugs not matching TODO.json — they'd be skipped gracefully
```

### LSP diagnostics

Clean — no errors or warnings.

## Key design decisions

1. **`_fetch_tuples`** (not `_read_tuples`): The plan text used the name `_fetch_tuples` and the code used `_read_tuples` inconsistently. Fixed to `_fetch_tuples` everywhere.

2. **Re-mapping foreign keys**: The migration builds `old_id → id_hash` mappings by first inserting persons/orgs into central (which computes content hashes), then looking up those hashes when inserting positions/relationships. For positions, `person_id` → `person_hash` via `old_id_to_hash`; for relationships, `person_a`/`person_b` → `person_a_hash`/`person_b_hash`.

3. **Resume support**: The `--resume` flag reads the `migration_audit` table in `registry.db` and skips slugs that have already been migrated.

4. **Province-aware switching**: Open one `Central` instance per province, flush registry stats on province switch. A `try/finally` block ensures the last province's partition is flushed even if processing is interrupted.

5. **No cross-province index**: As noted in the plan's self-review checklist, a cross-province index is deferred to a future optional task.