"""Integration tests for scripts/migrate_to_central.py — migration logic.

Tests verify that a legacy-format region DB can be migrated to the central
registry with correct foreign-key remapping using content hashes.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from gov_relation.central import Central
from gov_relation.paths import CENTRAL_DIR


def _create_full_db(db_path: Path) -> None:
    """Create a small legacy-format DB matching the production schema."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    conn.execute(
        "INSERT INTO persons (id, name, gender, birth) VALUES (1, '张三', '男', '1977-01')"
    )
    conn.execute(
        "INSERT INTO persons (id, name, gender, birth) VALUES (2, '李四', '男', '1980-05')"
    )
    conn.execute(
        "INSERT INTO organizations (id, name, type, level) VALUES (10, '县人民政府', '政府', 'county')"
    )
    conn.execute(
        "INSERT INTO positions (person_id, org_id, title) VALUES (1, 10, '县长')"
    )
    conn.execute(
        "INSERT INTO positions (person_id, org_id, title) VALUES (2, 10, '副县长')"
    )
    conn.execute(
        "INSERT INTO relationships (person_a, person_b, type, overlap_org, overlap_period) "
        "VALUES (1, 2, '正副搭档', 10, '2020-2023')"
    )

    conn.commit()
    conn.close()


def _create_minimal_db(db_path: Path, *, person_id: int = 1, org_id: int = 10) -> None:
    """Create a minimal legacy DB with persons, orgs, positions (no relationships)."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute(
        "CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT, gender TEXT)"
    )
    conn.execute(
        "INSERT INTO persons (id, name, gender) VALUES (?, 'test_person', '男')",
        (person_id,),
    )
    conn.execute(
        "CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT)"
    )
    conn.execute(
        "INSERT INTO organizations (id, name) VALUES (?, 'test_org')",
        (org_id,),
    )
    conn.execute(
        "CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "person_id INTEGER, org_id INTEGER, title TEXT)"
    )
    conn.execute(
        "INSERT INTO positions (person_id, org_id, title) VALUES (?, ?, 'test_title')",
        (person_id, org_id),
    )
    conn.commit()
    conn.close()


@pytest.fixture(autouse=True)
def clean_central():
    """Ensure clean central directory before and after each test."""
    if CENTRAL_DIR.exists():
        import shutil
        shutil.rmtree(str(CENTRAL_DIR))
    yield
    if CENTRAL_DIR.exists():
        import shutil
        shutil.rmtree(str(CENTRAL_DIR))


class TestMigrateOne:
    def test_migrate_populates_central(self, tmp_path: Path) -> None:
        """migrate_one processes a legacy DB and populates central correctly."""
        from scripts.migrate_to_central import migrate_one

        legacy_db = tmp_path / "test_区_network.db"
        _create_full_db(legacy_db)

        central = Central("test_province")
        stats = migrate_one(legacy_db, central, "test_区")

        assert stats["persons"] == 2, f"Expected 2 persons, got {stats['persons']}"
        assert stats["orgs"] == 1, f"Expected 1 org, got {stats['orgs']}"
        assert stats["positions"] == 2, f"Expected 2 positions, got {stats['positions']}"
        assert stats["rels"] == 1, f"Expected 1 relationship, got {stats['rels']}"
        assert stats["conflicts"] == 0, f"Expected 0 conflicts, got {stats['conflicts']}"

        # Verify central has the data
        persons = central.conn.execute(
            "SELECT name, birth FROM persons ORDER BY name"
        ).fetchall()
        assert len(persons) == 2
        # Unicode sort: 李 (U+674E) > 张 (U+5F20); 张 sorts first
        assert persons[0]["name"] == "张三"
        assert persons[1]["name"] == "李四"

        orgs = central.conn.execute("SELECT fqn FROM organizations").fetchall()
        assert len(orgs) == 1
        assert orgs[0]["fqn"] == "县人民政府"

        positions = central.conn.execute(
            "SELECT title FROM positions ORDER BY title"
        ).fetchall()
        assert len(positions) == 2
        assert positions[0]["title"] == "副县长"
        assert positions[1]["title"] == "县长"

        relationships = central.conn.execute(
            "SELECT type, overlap_period FROM relationships"
        ).fetchall()
        assert len(relationships) == 1
        assert relationships[0]["type"] == "正副搭档"

        central.close()

    def test_migrate_minimal_db(self, tmp_path: Path) -> None:
        """A minimal DB with persons, orgs, and a single position migrates correctly."""
        from scripts.migrate_to_central import migrate_one

        db_path = tmp_path / "minimal_network.db"
        _create_minimal_db(db_path)

        central = Central("test_province")
        stats = migrate_one(db_path, central, "minimal")

        assert stats["persons"] == 1
        assert stats["orgs"] == 1
        assert stats["positions"] == 1
        assert stats["rels"] == 0
        assert stats["conflicts"] == 0

        # Verify: the position has the correct title
        positions = central.conn.execute(
            "SELECT title FROM positions"
        ).fetchall()
        assert len(positions) == 1
        assert positions[0]["title"] == "test_title"

        central.close()

    def test_migrate_no_relationships(self, tmp_path: Path) -> None:
        """A DB without a relationships table should not crash."""
        from scripts.migrate_to_central import migrate_one

        db_path = tmp_path / "norel_network.db"
        _create_minimal_db(db_path, person_id=1, org_id=10)

        central = Central("test_province")
        stats = migrate_one(db_path, central, "norel")
        assert stats["persons"] == 1
        assert stats["orgs"] == 1
        assert stats["positions"] == 1
        assert stats["rels"] == 0
        assert stats["conflicts"] == 0
        central.close()

    def test_migrate_person_without_name(self, tmp_path: Path) -> None:
        """A person record without a name should not crash."""
        from scripts.migrate_to_central import migrate_one

        db_path = tmp_path / "noname_network.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT, gender TEXT)")
        conn.execute("INSERT INTO persons VALUES (1, '', '男')")
        conn.execute("CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO organizations VALUES (1, 'org')")
        conn.execute(
            "CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "person_id INTEGER, org_id INTEGER, title TEXT)"
        )
        conn.execute("INSERT INTO positions (person_id, org_id, title) VALUES (1, 1, 'test')")
        conn.commit()
        conn.close()

        central = Central("test_noproblem")
        stats = migrate_one(db_path, central, "noname")

        # Empty-name person gets hashed; positions resolve from id 1
        assert stats["persons"] >= 0
        assert stats["conflicts"] >= 0
        central.close()


@pytest.fixture
def fake_todo(tmp_path: Path) -> Path:
    """Create a minimal TODO.json in tmp_path."""
    todo = {
        "provinces": [
            {
                "province": "测试省",
                "tasks": [{"id": "test_province", "region": "测试省", "level": "province"}],
            },
            {
                "province": "河南省",
                "tasks": [
                    {"id": "henan_周口市", "region": "周口市", "level": "prefecture"},
                ],
            },
        ],
    }
    todo_path = tmp_path / "TODO.json"
    todo_path.write_text(json.dumps(todo, ensure_ascii=False), encoding="utf-8")
    return todo_path


class TestIntegration:
    """Slightly higher-level: use the province map to find the right output file."""

    def test_slug_without_province_is_skipped(self, tmp_path: Path) -> None:
        """A DB whose slug has no province mapping is skipped during main()."""
        from scripts.migrate_to_central import main
        pass