"""Tests for the v3 schema factory."""

import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from gov_relation.factory import SchemaFactory


def test_create_all_builds_21_tables_and_v3_columns(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(conn)
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    assert len(tables) == 21
    assert {"education", "merged_into_id"} <= {
        row[1] for row in conn.execute("PRAGMA table_info(persons)")
    }
    assert {"title_category", "sort_order"} <= {
        row[1] for row in conn.execute("PRAGMA table_info(positions)")
    }
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == "3.0.0"


def test_create_all_is_idempotent(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    factory = SchemaFactory()
    factory.create_all(conn)
    factory.create_all(conn)


def test_foreign_keys_are_enforced(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(conn)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO positions(position_id, person_id) VALUES(?, ?)",
            ("pos_missing", "per_missing"),
        )


def test_commercial_view_uses_only_latest_effective_decision(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(conn)
    conn.execute("INSERT INTO sources(source_id) VALUES('src_1')")
    now = datetime.now(timezone.utc)
    for index, (decision, uses) in enumerate(
        (("cleared", '["commercial_distribution"]'), ("restricted", "[]")),
        start=1,
    ):
        effective = (now - timedelta(days=3 - index)).isoformat()
        manifest = f"manifest_{index}"
        conn.execute(
            """INSERT INTO rights_manifests(
                   manifest_id, schema_version, payload_sha256,
                   signature_algorithm, signature_key_id, signature_base64,
                   created_at, reviewed_by, review_authority, effective_from
               ) VALUES(?, '1', 'hash', 'test', 'key', 'signature', ?, 'r', 'a', ?)""",
            (manifest, effective, effective),
        )
        conn.execute(
            """INSERT INTO source_rights_decisions(
                   decision_row_id, decision_id, manifest_id, source_id,
                   decision, permitted_uses_json, permitted_fields_json,
                   restrictions_json, rationale, effective_from
               ) VALUES(?, 'same', ?, 'src_1', ?, ?, '[]', '[]', 'test', ?)""",
            (f"row_{index}", manifest, decision, uses, effective),
        )
    assert conn.execute(
        "SELECT COUNT(*) FROM gold_commercial_sources"
    ).fetchone()[0] == 0
