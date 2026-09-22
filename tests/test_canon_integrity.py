"""Regression tests for the canonical JSONL/SQLite consistency boundary."""

from __future__ import annotations

import json
import sqlite3

import pytest

from gov_relation.canon.engine import (
    content_tables_from_dir,
    export_db_to_records,
    rebuild_db_from_records,
    verify_consistency,
)
from gov_relation.canon.streams import quote_identifier


def test_metadata_table_is_not_a_canonical_stream(tmp_path):
    source = tmp_path / "source.db"
    with sqlite3.connect(source) as conn:
        conn.executescript(
            "CREATE TABLE persons (person_id TEXT PRIMARY KEY);"
            "CREATE TABLE schema_meta (key TEXT PRIMARY KEY, value TEXT);"
        )
        conn.execute("INSERT INTO persons VALUES ('p1')")
    records = tmp_path / "records"
    export_db_to_records(source, records)
    assert content_tables_from_dir(records) == ["persons"]
    assert not (records / "schema_meta.jsonl").exists()
    backup = tmp_path / "backup.db"
    rebuild_db_from_records(records, backup)
    # A derived database may contain its own metadata without a JSONL stream.
    with sqlite3.connect(backup) as conn:
        conn.execute("CREATE TABLE schema_meta (key TEXT, value TEXT)")
    result = verify_consistency(records, backup)
    assert result["consistent"] is True
    assert result["_extra_tables"] == []


def test_missing_content_table_is_reported_not_raised(tmp_path):
    source = tmp_path / "source.db"
    with sqlite3.connect(source) as conn:
        conn.execute("CREATE TABLE persons (person_id TEXT)")
        conn.execute("INSERT INTO persons VALUES ('p1')")
    records = tmp_path / "records"
    export_db_to_records(source, records)
    missing_backup = tmp_path / "missing.db"
    with sqlite3.connect(missing_backup) as conn:
        conn.execute("CREATE TABLE unrelated (value TEXT)")
    result = verify_consistency(records, missing_backup)
    assert result["consistent"] is False
    assert result["_missing_tables"] == ["persons"]
    assert result["_extra_tables"] == ["unrelated"]
    assert result["persons"]["ok"] is False
    assert result["persons"]["db_count"] is None


def test_sqlite_identifiers_roundtrip_with_keywords_and_quotes(tmp_path):
    source = tmp_path / "source.db"
    with sqlite3.connect(source) as conn:
        conn.execute('CREATE TABLE "odd""table" ("select" TEXT, "title""name" TEXT)')
        conn.execute('INSERT INTO "odd""table" VALUES (?, ?)', ("x", "y"))
    records = tmp_path / "records"
    export_db_to_records(source, records)
    backup = tmp_path / "backup.db"
    rebuild_db_from_records(records, backup)
    assert verify_consistency(records, backup)["consistent"] is True
    with sqlite3.connect(backup) as conn:
        assert conn.execute('SELECT "select", "title""name" FROM "odd""table"').fetchone() == ("x", "y")


def test_quote_identifier_rejects_invalid_names():
    assert quote_identifier('a"b') == '"a""b"'
    for invalid in ("", "bad\x00name", None):
        with pytest.raises(ValueError):
            quote_identifier(invalid)


def test_rebuild_rejects_unexpected_later_columns_without_replacing_backup(tmp_path):
    source = tmp_path / "source.db"
    with sqlite3.connect(source) as conn:
        conn.execute("CREATE TABLE persons (person_id TEXT, name TEXT)")
        conn.execute("INSERT INTO persons VALUES ('p1', 'Alice')")
    records = tmp_path / "records"
    export_db_to_records(source, records)
    backup = tmp_path / "backup.db"
    rebuild_db_from_records(records, backup)
    previous_bytes = backup.read_bytes()
    (records / "persons.jsonl").write_text(
        json.dumps({"person_id": "p1"}) + "\n"
        + json.dumps({"person_id": "p2", "name": "Bob"}) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Unexpected columns"):
        rebuild_db_from_records(records, backup, overwrite=True)
    assert backup.read_bytes() == previous_bytes
