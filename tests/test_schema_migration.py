"""Regression tests for the explicit v2 to v3 schema migration and the
create_schema() v3-shape gate."""

import importlib.util
import sqlite3
from pathlib import Path

import pytest

from gov_relation.platform.schema import DDL, create_schema, has_v3_shape


def _migration_module():
    path = Path("scripts/migrate/upgrade_schema_v2_to_v3.py").resolve()
    spec = importlib.util.spec_from_file_location("upgrade_v3", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _v2_ddl() -> str:
    """Platform v3 DDL stripped of the v3-only columns (a v2-shaped schema)."""
    v2 = DDL
    for line in (
        "    commercial_use INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use IN (0, 1)),\n",
        "    education TEXT NOT NULL DEFAULT '',\n",
        "    merged_into_id TEXT REFERENCES persons(person_id),\n",
        "    title_category TEXT NOT NULL DEFAULT '',\n",
        "    sort_order INTEGER NOT NULL DEFAULT 0,\n",
    ):
        v2 = v2.replace(line, "")
    return v2


def _v2_database(path: Path) -> None:
    conn = sqlite3.connect(path)
    conn.executescript(_v2_ddl())
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta VALUES('schema_version', '2.1.0')"
    )
    conn.execute(
        """INSERT INTO persons(person_id, canonical_name, normalized_name)
           VALUES('per_1', '甲', '甲')"""
    )
    conn.execute(
        """INSERT INTO positions(position_id, person_id, category)
           VALUES('pos_1', 'per_1', '党委正职')"""
    )
    conn.commit()
    conn.close()


def test_dry_run_reports_without_modifying(tmp_path):
    path = tmp_path / "v2.db"
    _v2_database(path)
    migration = _migration_module()
    result = migration.upgrade(path, dry_run=True)
    assert result["status"] == "dry-run"
    conn = sqlite3.connect(path)
    assert "education" not in {
        row[1] for row in conn.execute("PRAGMA table_info(persons)")
    }
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "2.1.0"


def test_dry_run_does_not_create_a_missing_database(tmp_path):
    path = tmp_path / "missing.db"
    migration = _migration_module()
    with pytest.raises(sqlite3.OperationalError):
        migration.upgrade(path, dry_run=True)
    assert not path.exists()


def test_upgrade_is_shape_aware_backfills_and_is_idempotent(tmp_path):
    path = tmp_path / "v2.db"
    _v2_database(path)
    migration = _migration_module()
    result = migration.upgrade(path)
    assert result["status"] == "upgraded"
    backup = Path(result["backup"])
    assert backup.exists()
    backup_conn = sqlite3.connect(backup)
    assert backup_conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "2.1.0"
    backup_conn.close()
    conn = sqlite3.connect(path)
    assert migration.has_v3_shape(conn)
    assert conn.execute(
        "SELECT title_category FROM positions WHERE position_id='pos_1'"
    ).fetchone()[0] == "党委正职"
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "3.0.0"
    conn.close()
    assert migration.upgrade(path)["status"] == "skipped"


def test_create_schema_refuses_unversioned_v2_database(tmp_path):
    """An unstamped (no schema_meta table) v2-shaped DB must not be stamped 3.0.0."""
    path = tmp_path / "unversioned.db"
    conn = sqlite3.connect(path)
    conn.executescript(_v2_ddl())
    conn.commit()
    assert not has_v3_shape(conn)
    with pytest.raises(RuntimeError, match="lacks the required v3 columns"):
        create_schema(conn)
    conn.close()
    conn = sqlite3.connect(path)
    assert conn.execute(
        "SELECT COUNT(*) FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == 0
    conn.close()


def test_create_schema_refuses_unstamped_v2_database_with_meta_table(tmp_path):
    """schema_meta exists but the version row is missing: still requires v3 shape."""
    path = tmp_path / "unstamped.db"
    conn = sqlite3.connect(path)
    conn.executescript(_v2_ddl())
    assert conn.execute(
        "SELECT 1 FROM sqlite_master WHERE name='schema_meta'"
    ).fetchone()
    with pytest.raises(RuntimeError, match="upgrade_schema_v2_to_v3"):
        create_schema(conn)
    conn.close()


def test_create_schema_still_initializes_a_fresh_empty_database(tmp_path):
    """Brand-new empty databases keep working (init / build on a fresh path)."""
    path = tmp_path / "fresh.db"
    conn = sqlite3.connect(path)
    create_schema(conn)
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "3.0.0"
    assert has_v3_shape(conn)
    conn.close()


def test_create_schema_stamps_an_unstamped_v3_shaped_database(tmp_path):
    """An unversioned database that already has the v3 shape is stamped."""
    path = tmp_path / "v3-unstamped.db"
    conn = sqlite3.connect(path)
    conn.executescript(DDL)
    conn.commit()
    assert has_v3_shape(conn)
    create_schema(conn)
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "3.0.0"
    conn.close()


def test_create_schema_accepts_stamped_v3_database(tmp_path):
    """Stamped 3.0.0 databases pass unchanged."""
    path = tmp_path / "stamped.db"
    conn = sqlite3.connect(path)
    conn.executescript(DDL)
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta VALUES('schema_version', '3.0.0')"
    )
    conn.commit()
    create_schema(conn)
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "3.0.0"
    conn.close()


def test_create_schema_rejects_stamped_incompatible_version_even_with_v3_shape(tmp_path):
    """Stamped 2.1.0 stays incompatible even if the columns happen to be v3-shaped."""
    path = tmp_path / "old-stamp.db"
    conn = sqlite3.connect(path)
    conn.executescript(DDL)
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta VALUES('schema_version', '2.1.0')"
    )
    conn.commit()
    assert has_v3_shape(conn)
    with pytest.raises(RuntimeError, match="2.1.0"):
        create_schema(conn)
    conn.close()


def test_create_schema_keeps_legacy_behavior_for_stamped_v3_without_shape(tmp_path):
    """A DB stamped 3.0.0 but lacking v3 columns is not rejected (legacy behavior)."""
    path = tmp_path / "false-stamp.db"
    conn = sqlite3.connect(path)
    conn.executescript(_v2_ddl())
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta VALUES('schema_version', '3.0.0')"
    )
    conn.commit()
    create_schema(conn)  # must not raise
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "3.0.0"
    conn.close()
