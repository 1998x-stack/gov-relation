# Task 6 Report: Runner extension

**Status:** DONE

**Commit:** `baa722c6` — `feat: add optional central param to run_build()`

## Files changed

| File | Change |
|------|--------|
| `gov_relation/runner.py` | Added `central: Any = None` param to `run_build()` signature; added central-registry write loop after GEXF block |
| `tests/test_runner.py` | Added `TestRunBuildWithCentralOpt` class with 2 test methods |

## Test summary

```
tests/test_runner.py::TestRunBuild::test_creates_db_and_gexf           PASSED
tests/test_runner.py::TestRunBuild::test_db_has_correct_data           PASSED
tests/test_runner.py::TestRunBuild::test_overwrite_replaces_db         PASSED
tests/test_runner.py::TestRunBuild::test_gexf_contains_nodes_and_edges PASSED
tests/test_runner.py::TestRunBuildWithCentralOpt::test_central_param_does_not_break_basic PASSED
tests/test_runner.py::TestRunBuildWithCentralOpt::test_central_param_does_not_crash    PASSED
```

**6 passed, 0 failed** — all existing tests remain green; both new tests pass.

## What was done

1. **TDD RED phase:** Wrote `TestRunBuildWithCentralOpt` with two tests — the first verifies that calling `run_build()` without `central=` still works (backward-compat), the second verifies that passing a `Central` instance doesn't crash.

2. **GREEN implementation**:
   - Added `central: Any = None` as an optional keyword-only parameter (default `None` means **zero impact on existing callers**)
   - After the GEXF builder writes its file, inserted the loop that calls `merge_person`, `merge_organization`, `insert_position`, `insert_relationship` on the central writer for each data list

3. **Verification**: All 6 tests pass, LSP diagnostics clean.