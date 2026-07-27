"""Tests for gov_relation/central.py — Central registry writer class."""

from __future__ import annotations

import sqlite3
from collections.abc import Generator

import pytest

from gov_relation.central import Central
from gov_relation.paths import CENTRAL_DIR, PROVINCE_DIR


@pytest.fixture(autouse=True)
def cleanup_central():
    """Remove any leftover central data before/after tests."""
    if CENTRAL_DIR.exists():
        import shutil
        shutil.rmtree(str(CENTRAL_DIR))
    yield
    if CENTRAL_DIR.exists():
        import shutil
        shutil.rmtree(str(CENTRAL_DIR))


class TestCentral:
    @pytest.fixture
    def central(self) -> Generator[Central, None, None]:
        c = Central("test_province")
        yield c
        c.close()

    def test_merge_person_returns_hash(self, central: Central) -> None:
        h = central.merge_person({"name": "张三", "birth": "1977-01"})
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)

    def test_merge_same_person_returns_same_hash(self, central: Central) -> None:
        h1 = central.merge_person({"name": "张三", "birth": "1977-01"})
        h2 = central.merge_person({"name": "张三", "birth": "1977-01"})
        assert h1 == h2

    def test_merge_person_upserts_fields(self, central: Central) -> None:
        h = central.merge_person({"name": "张三", "birth": "1977-01", "gender": "男"})
        central.merge_person({"name": "张三", "birth": "1977-01", "education": "研究生"})
        row = central.conn.execute(
            "SELECT education FROM persons WHERE id_hash=?", (h,)
        ).fetchone()
        assert row[0] == "研究生"
        # Gender was not overwritten
        row2 = central.conn.execute(
            "SELECT gender FROM persons WHERE id_hash=?", (h,)
        ).fetchone()
        assert row2[0] == "男"

    def test_merge_org_returns_hash(self, central: Central) -> None:
        h = central.merge_organization({"fqn": "周口市人民政府", "province": "test_province"})
        assert len(h) == 16

    def test_insert_position(self, central: Central) -> None:
        p_h = central.merge_person({"name": "张三", "birth": "1977-01"})
        o_h = central.merge_organization({"fqn": "周口市人民政府", "province": "test_province"})
        pos_id = central.insert_position({
            "person_hash": p_h,
            "org_hash": o_h,
            "title": "市长",
            "province": "test_province",
        })
        assert pos_id is not None

    def test_insert_relationship(self, central: Central) -> None:
        p1 = central.merge_person({"name": "张三", "birth": "1977-01"})
        p2 = central.merge_person({"name": "李四", "birth": "1980-05"})
        rid = central.insert_relationship({
            "person_a_hash": p1,
            "person_b_hash": p2,
            "type": "正副搭档",
            "province": "test_province",
        })
        assert rid is not None

    def test_flush_registry_updates_counts(self, central: Central, tmp_path) -> None:
        central.merge_person({"name": "张三", "birth": "1977-01"})
        central.merge_organization({"fqn": "人民政府", "province": "test_province"})
        registry_path = str(tmp_path / "test_registry.db")
        central.flush_registry(registry_path)

        reg = sqlite3.connect(registry_path)
        reg.row_factory = sqlite3.Row
        row = reg.execute(
            "SELECT * FROM region_registry WHERE province='test_province'"
        ).fetchone()
        assert row is not None
        assert row["person_count"] >= 1
        reg.close()