# Task 1 Report: Hash functions

## Summary

Implemented `gov_relation/hash.py` with three functions:
- `normalize(s: str | None) -> str` — NFKC normalization + strip
- `person_hash(name: str, birth: str) -> str` — SHA256 hex[:16] of `normalize(name) + "|" + birth`
- `org_hash(province: str, fqn: str) -> str` — SHA256 hex[:16] of `province + "|" + normalize(fqn)`

Also updated `gov_relation/__init__.py` to export the three hash functions.

## Test Results

```
$ PYTHONPATH=. python3 -m pytest tests/test_hash.py -v
```

```
tests/test_hash.py::TestNormalize::test_trims_whitespace PASSED
tests/test_hash.py::TestNormalize::test_wide_to_half_converted PASSED
tests/test_hash.py::TestNormalize::test_empty_string PASSED
tests/test_hash.py::TestNormalize::test_none_becomes_empty PASSED
tests/test_hash.py::TestPersonHash::test_same_name_birth_same_hash PASSED
tests/test_hash.py::TestPersonHash::test_different_birth_different_hash PASSED
tests/test_hash.py::TestPersonHash::test_empty_birth_uses_empty_string PASSED
tests/test_hash.py::TestPersonHash::test_name_normalized PASSED
tests/test_hash.py::TestPersonHash::test_returns_16_hex_chars PASSED
tests/test_hash.py::TestOrgHash::test_same_fqn_same_hash PASSED
tests/test_hash.py::TestOrgHash::test_different_province_different_hash PASSED
tests/test_hash.py::TestOrgHash::test_returns_16_hex_chars PASSED
============================== 12 passed in 0.06s ==============================
```

Full suite: 139 passed, 0 failed.

## Concerns

- **Wide-space test adjusted:** The plan's `test_unifies_wide_to_half` expected `normalize("张　三") == "张三"` but per the spec (`unicodedata.normalize("NFKC", s).strip()`), NFKC converts U+3000 (ideographic space) → U+0020 (space), yielding `"张 三"`, and `strip()` only trims leading/trailing whitespace. The test was changed to verify NFKC conversion happens and result is stripped, which is consistent with the published interface. If internal whitespace collapsing is desired, `normalize()` would need an additional `re.sub(r'\s+', '', s)` — this should be decided before downstream tasks consume it.

## Commit

```
2eeae847 feat: add content-hash functions for person/org dedup
```

## Files Changed

- Created: `gov_relation/hash.py` (26 lines)
- Created: `tests/test_hash.py` (86 lines)
- Modified: `gov_relation/__init__.py` (3 lines added)