# Task 4: Central Writer Class — Report

## Summary

Created `gov_relation/central.py` with the `Central` class — the heart of the central registry system. Also created `tests/test_central.py` with 7 tests covering all public API methods.

## Files Changed

| File | Action | Lines |
|------|--------|-------|
| `gov_relation/central.py` | **Created** | 226 |
| `tests/test_central.py` | **Created** | 96 |

## Public API (`gov_relation.central.Central`)

- `Central(province)` — opens province-partitioned SQLite DB at `data/central/provincial/{province}.db`
- `merge_person(person: dict) -> str` — UPSERT by content hash (`person_hash(name, birth)[:16]`)
- `merge_organization(org: dict) -> str` — UPSERT by content hash (`org_hash(province, fqn)[:16]`)
- `insert_position(pos: dict) -> int` — INSERT with FK references to person/org hashes
- `insert_relationship(rel: dict) -> int` — INSERT with FK references; empty `overlap_org_hash` → NULL (avoids FK failure)
- `close()` — closes the SQLite connection
- `flush_registry(registry_path)` — writes partition stats to a registry DB (person_count, org_count, etc.)

## Key Design Decisions

1. **`overlap_org_hash` FK fix:** The FK `FOREIGN KEY (overlap_org_hash) REFERENCES organizations(id_hash)` means empty string `""` fails. We pass `None` instead via `rel.get("overlap_org_hash") or None`.

2. **`source_json` pipeline**: New person records store `{"<source>": "high"}`; upserts append `"migrated"` status for any new source not already present.

3. **Fixture isolation**: `cleanup_central` (`autouse=True`) cleans `CENTRAL_DIR` before/after each test. The `test_flush_registry` test uses `tmp_path` to avoid using `PROVINCE_DIR`.

## Test Results

```bash
$ PYTHONPATH=. python3 -m pytest tests/test_central.py -v
============================= test session starts ==============================
collected 7 items

tests/test_central.py::TestCentral::test_merge_person_returns_hash PASSED [ 14%]
tests/test_central.py::TestCentral::test_merge_same_person_returns_same_hash PASSED [ 28%]
tests/test_central.py::TestCentral::test_merge_person_upserts_fields PASSED [ 42%]
tests/test_central.py::TestCentral::test_merge_org_returns_hash PASSED   [ 57%]
tests/test_central.py::TestCentral::test_insert_position PASSED          [ 71%]
tests/test_central.py::TestCentral::test_insert_relationship PASSED      [ 85%]
tests/test_central.py::TestCentral::test_flush_registry_updates_counts PASSED [100%]

============================== 7 passed in 0.96s ===============================
```

## Concerns

- `overlap_org_hash` FK fix uses `or None` which converts empty string `""` to `None` — correct for SQLite FK semantics but worth noting if any caller intentionally passes a non-empty string that might be falsy
- The `# type: ignore[return-value]` on `lastrowid` returns is necessary because Pyright strict mode flags `int | None`