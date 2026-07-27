# Task 5: Province Detection — Report

**Status:** DONE

## Files Created
- `gov_relation/province.py` — `build_slug_province_map()` and `detect_province()`
- `tests/test_province.py` — 3 tests

## Interfaces
- `build_slug_province_map(todo_path: Path | None = None) -> dict[str, str]`
- `detect_province(slug: str, todo_path: Path | None = None, map_cache: dict[str, str] | None = None) -> str`

## Test Results (RED → GREEN)
```
RED:  ModuleNotFoundError — gov_relation.province doesn't exist
GREEN: 3/3 passed (TestDetectProvince::test_known_slugs, test_unknown_slug_raises, TestBuildMapFromTodo::test_from_todo_json)
```

## Commit SHA
`72a887e7`