# Task 3: Central paths — Report

**Status:** DONE

**Files changed:**
- `gov_relation/paths.py` — added `CENTRAL_DIR`, `REGISTRY_DB`, `PROVINCE_DIR`
- `tests/test_paths.py` — added `TestCentralPaths` (2 test methods)

## Test results

```
$ PYTHONPATH=. python3 -m pytest tests/test_paths.py -v
============================= 12 passed in 0.06s ==============================
```

- All 10 pre-existing tests: PASS
- 2 new `TestCentralPaths` tests: PASS
- No regressions.

## Commit

```
d350ef55e040b243aae0cab504e2860c24194db7
feat: add central registry paths (CENTRAL_DIR, REGISTRY_DB, PROVINCE_DIR)
```

## Concerns

None. Straightforward addition of 3 constants and 2 tests following exact plan spec.