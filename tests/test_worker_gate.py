"""Gate tests for `scripts/govdb.py build_database`.

build_database refuses to build over an existing destination that is not a
stamped, v3-shaped canonical database — even with `--replace` — pointing the
operator at scripts/migrate/upgrade_schema_v2_to_v3.py.
"""

from __future__ import annotations

import argparse
import importlib.util
import sqlite3
from pathlib import Path

import pytest

from gov_relation.platform.schema import DDL


def _govdb_module():
    path = Path("scripts/govdb.py").resolve()
    spec = importlib.util.spec_from_file_location("govdb", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _v2_database(path: Path) -> None:
    v2 = DDL
    for line in (
        "    commercial_use INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use IN (0, 1)),\n",
        "    education TEXT NOT NULL DEFAULT '',\n",
        "    merged_into_id TEXT REFERENCES persons(person_id),\n",
        "    title_category TEXT NOT NULL DEFAULT '',\n",
        "    sort_order INTEGER NOT NULL DEFAULT 0,\n",
    ):
        v2 = v2.replace(line, "")
    conn = sqlite3.connect(path)
    conn.executescript(v2)
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta VALUES('schema_version', '2.1.0')"
    )
    conn.commit()
    conn.close()


def _v3_database(path: Path) -> None:
    conn = sqlite3.connect(path)
    conn.executescript(DDL)
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta VALUES('schema_version', '3.0.0')"
    )
    conn.commit()
    conn.close()


def _build_args(
    govdb, database: Path, *, replace: bool = True
) -> argparse.Namespace:
    legacy_dir = database.parent / "legacy"
    profiles_dir = database.parent / "profiles"
    legacy_dir.mkdir(exist_ok=True)
    profiles_dir.mkdir(exist_ok=True)
    return argparse.Namespace(
        database=database,
        replace=replace,
        legacy_dir=legacy_dir,
        profiles_dir=profiles_dir,
        limit=0,
        progress=0,
    )


def test_build_refuses_v2_destination_even_with_replace(tmp_path):
    """--replace must not clobber an unmigrated v2 database."""
    govdb = _govdb_module()
    destination = tmp_path / "gov_relation.db"
    _v2_database(destination)
    args = _build_args(govdb, destination, replace=True)
    with pytest.raises(SystemExit) as excinfo:
        govdb.build_database(args)
    message = str(excinfo.value)
    assert "not a v3-shaped canonical database" in message
    assert "upgrade_schema_v2_to_v3.py" in message
    # The destination was left untouched.
    conn = sqlite3.connect(destination)
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "2.1.0"
    conn.close()


def test_build_refuses_unstamped_destination_even_with_replace(tmp_path):
    """An existing file without a 3.0.0 stamp is refused even with --replace."""
    govdb = _govdb_module()
    destination = tmp_path / "unstamped.db"
    _v3_database(destination)
    conn = sqlite3.connect(destination)
    conn.execute("DELETE FROM schema_meta WHERE key='schema_version'")
    conn.commit()
    conn.close()
    args = _build_args(govdb, destination, replace=True)
    with pytest.raises(SystemExit, match="upgrade_schema_v2_to_v3.py"):
        govdb.build_database(args)


def test_build_refuses_false_stamped_v3_destination_even_with_replace(tmp_path):
    """A 3.0.0 stamp without the v3 columns (older create_schema) is refused."""
    govdb = _govdb_module()
    destination = tmp_path / "false-stamp.db"
    v2 = DDL
    for line in (
        "    commercial_use INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use IN (0, 1)),\n",
        "    education TEXT NOT NULL DEFAULT '',\n",
        "    merged_into_id TEXT REFERENCES persons(person_id),\n",
        "    title_category TEXT NOT NULL DEFAULT '',\n",
        "    sort_order INTEGER NOT NULL DEFAULT 0,\n",
    ):
        v2 = v2.replace(line, "")
    conn = sqlite3.connect(destination)
    conn.executescript(v2)
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta VALUES('schema_version', '3.0.0')"
    )
    conn.commit()
    conn.close()
    args = _build_args(govdb, destination, replace=True)
    with pytest.raises(SystemExit, match="upgrade_schema_v2_to_v3.py"):
        govdb.build_database(args)


def test_build_requires_replace_for_v3_destination(tmp_path):
    """A v3-shaped destination still needs --replace (existing behavior)."""
    govdb = _govdb_module()
    destination = tmp_path / "v3.db"
    _v3_database(destination)
    args = _build_args(govdb, destination, replace=False)
    with pytest.raises(SystemExit, match="use --replace"):
        govdb.build_database(args)


def test_build_over_v3_destination_with_replace_succeeds(tmp_path, capsys):
    """--replace over a stamped v3-shaped destination keeps working."""
    govdb = _govdb_module()
    destination = tmp_path / "existing.db"
    _v3_database(destination)
    args = _build_args(govdb, destination, replace=True)
    result = govdb.build_database(args)
    capsys.readouterr()
    assert result == 0
    conn = sqlite3.connect(destination)
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "3.0.0"
    conn.close()