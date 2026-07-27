"""Tests for gov_relation/hash.py — content-hash functions for person/org dedup."""

from __future__ import annotations

import pytest

from gov_relation.hash import normalize, person_hash, org_hash


class TestNormalize:
    def test_trims_whitespace(self) -> None:
        assert normalize("  张三  ") == "张三"

    def test_wide_to_half_converted(self) -> None:
        # NFKC converts ideographic space (U+3000) → space, then re collapses it
        result = normalize("张　三")
        assert result == "张三"

    def test_empty_string(self) -> None:
        assert normalize("") == ""

    def test_none_becomes_empty(self) -> None:
        assert normalize(None) == ""


class TestPersonHash:
    def test_same_name_birth_same_hash(self) -> None:
        assert person_hash("张三", "1977-01") == person_hash("张三", "1977-01")

    def test_different_birth_different_hash(self) -> None:
        assert person_hash("张三", "1977-01") != person_hash("张三", "1980-05")

    def test_empty_birth_uses_empty_string(self) -> None:
        h = person_hash("张三", "")
        assert len(h) == 16

    def test_name_normalized(self) -> None:
        assert person_hash("  张三  ", "1977-01") == person_hash("张三", "1977-01")

    def test_returns_16_hex_chars(self) -> None:
        h = person_hash("张三", "1977-01")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)


class TestOrgHash:
    def test_same_fqn_same_hash(self) -> None:
        assert org_hash("河南省", "周口市人民政府") == org_hash("河南省", "周口市人民政府")

    def test_different_province_different_hash(self) -> None:
        assert org_hash("河南省", "周口市人民政府") != org_hash("湖北省", "周口市人民政府")

    def test_returns_16_hex_chars(self) -> None:
        h = org_hash("广东省", "深圳市人民政府")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)