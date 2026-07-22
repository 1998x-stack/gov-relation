"""Tests for gov_relation/schema.py."""

from __future__ import annotations

import sqlite3

import pytest

from gov_relation.schema import (
    create_tables,
    insert_organizations,
    insert_persons,
    insert_positions,
    insert_relationships,
)


@pytest.fixture
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    create_tables(c)
    return c


class TestCreateTables:
    def test_creates_four_tables(self, conn: sqlite3.Connection) -> None:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name"
        ).fetchall()
        names = [r[0] for r in tables]
        assert names == ["organizations", "persons", "positions", "relationships"]

    def test_overwrite_drops_existing(self, conn: sqlite3.Connection) -> None:
        # Insert some data
        insert_persons(conn, [{"id": 1, "name": "张三"}])
        # Overwrite
        create_tables(conn, overwrite=True)
        count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        assert count == 0

    def test_idempotent_create(self, conn: sqlite3.Connection) -> None:
        # Calling create_tables twice should not fail
        create_tables(conn)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'"
        ).fetchall()
        assert len(tables) == 4


class TestInsertPersons:
    def test_inserts_single(self, conn: sqlite3.Connection) -> None:
        id_map = insert_persons(conn, [{"id": 1, "name": "张三"}])
        assert 1 in id_map
        row = conn.execute("SELECT name FROM persons WHERE id=?", (id_map[1],)).fetchone()
        assert row[0] == "张三"

    def test_inserts_multiple(self, conn: sqlite3.Connection) -> None:
        persons = [
            {"id": 1, "name": "张三", "gender": "男"},
            {"id": 2, "name": "李四", "gender": "女"},
        ]
        id_map = insert_persons(conn, persons)
        assert len(id_map) == 2
        rows = conn.execute("SELECT name FROM persons ORDER BY id").fetchall()
        assert [r[0] for r in rows] == ["张三", "李四"]

    def test_returns_id_mapping(self, conn: sqlite3.Connection) -> None:
        id_map = insert_persons(conn, [{"id": 42, "name": "王五"}])
        assert id_map[42] is not None
        # Since persons uses INTEGER PRIMARY KEY (not AUTOINCREMENT),
        # SQLite reuses the provided id value in this case
        assert id_map[42] == 42

    def test_defaults_empty_fields(self, conn: sqlite3.Connection) -> None:
        id_map = insert_persons(conn, [{"id": 1, "name": "赵六"}])
        row = conn.execute("SELECT * FROM persons WHERE id=?", (id_map[1],)).fetchone()
        # gender should default to empty string, not None
        assert row["gender"] == ""


class TestInsertOrganizations:
    def test_inserts_single(self, conn: sqlite3.Connection) -> None:
        id_map = insert_organizations(conn, [{"id": 1, "name": "县委"}])
        assert 1 in id_map

    def test_org_with_all_fields(self, conn: sqlite3.Connection) -> None:
        orgs = [{"id": 1, "name": "市政府", "type": "government", "level": "prefecture", "parent": "省政府", "location": "南昌"}]
        insert_organizations(conn, orgs)
        row = conn.execute("SELECT * FROM organizations").fetchone()
        assert row["type"] == "government"
        assert row["level"] == "prefecture"


class TestInsertPositions:
    def test_inserts_position(self, conn: sqlite3.Connection) -> None:
        p_map = insert_persons(conn, [{"id": 1, "name": "甲"}])
        o_map = insert_organizations(conn, [{"id": 10, "name": "县政府"}])
        insert_positions(conn, [{"person_id": p_map[1], "org_id": o_map[10], "title": "县长"}])
        rows = conn.execute("SELECT title FROM positions").fetchall()
        assert [r[0] for r in rows] == ["县长"]

    def test_foreign_key_enforced(self, conn: sqlite3.Connection) -> None:
        conn.execute("PRAGMA foreign_keys = ON")
        with pytest.raises(sqlite3.IntegrityError):
            insert_positions(conn, [{"person_id": 999, "org_id": 888, "title": "虚拟岗位"}])


class TestInsertRelationships:
    def test_inserts_relationship(self, conn: sqlite3.Connection) -> None:
        pm = insert_persons(conn, [{"id": 1, "name": "甲"}, {"id": 2, "name": "乙"}])
        insert_relationships(conn, [{"person_a": pm[1], "person_b": pm[2], "type": "共事", "context": "同届党委"}])
        rows = conn.execute("SELECT type, context FROM relationships").fetchall()
        assert [(r[0], r[1]) for r in rows] == [("共事", "同届党委")]

    def test_foreign_key_enforced(self, conn: sqlite3.Connection) -> None:
        conn.execute("PRAGMA foreign_keys = ON")
        with pytest.raises(sqlite3.IntegrityError):
            insert_relationships(conn, [{"person_a": 999, "person_b": 888, "type": "虚拟"}])


class TestEndToEnd:
    def test_full_insert_cycle(self, conn: sqlite3.Connection) -> None:
        pm = insert_persons(conn, [
            {"id": 1, "name": "张三", "gender": "男"},
            {"id": 2, "name": "李四", "gender": "女"},
        ])
        om = insert_organizations(conn, [{"id": 10, "name": "县政府"}])
        insert_positions(conn, [
            {"person_id": pm[1], "org_id": om[10], "title": "县长"},
            {"person_id": pm[2], "org_id": om[10], "title": "副县长"},
        ])
        insert_relationships(conn, [{"person_a": pm[1], "person_b": pm[2], "type": "共事"}])

        assert conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0] == 2
        assert conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 2
        assert conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0] == 1
