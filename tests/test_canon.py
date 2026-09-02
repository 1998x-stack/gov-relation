"""Tests for the canonical JSONL + SQLite backup engine."""

from __future__ import annotations

import json

import pytest

from gov_relation.canon.engine import (
    export_db_to_records,
    rebuild_db_from_records,
    verify_consistency,
)
from gov_relation.canon import streams


def _make_db(path):
    conn = __import__("sqlite3").connect(str(path))
    conn.executescript(
        """
        CREATE TABLE persons (
            person_id TEXT PRIMARY KEY,
            canonical_name TEXT,
            province TEXT
        );
        CREATE TABLE positions (
            position_id TEXT PRIMARY KEY,
            person_id TEXT,
            title TEXT
        );
        """
    )
    conn.executemany(
        "INSERT INTO persons VALUES (?,?,?)",
        [("p1", "张三", "广东省"), ("p2", "李四", "广东省")],
    )
    conn.executemany(
        "INSERT INTO positions VALUES (?,?,?)",
        [("p1pos0", "p1", "书记"), ("p2pos0", "p2", "市长")],
    )
    conn.commit()
    conn.close()
    return str(path)


def test_roundtrip_is_byte_for_byte_consistent(tmp_path):
    src = _make_db(tmp_path / "src.db")
    records = tmp_path / "records"
    export_db_to_records(src, records)

    backup = tmp_path / "backup.db"
    rebuild_db_from_records(records, backup, overwrite=True)
    result = verify_consistency(records, backup)
    assert result["consistent"] is True
    assert result["_missing_tables"] == []
    assert result["_extra_tables"] == []
    for key, meta in result.items():
        if isinstance(meta, dict):
            assert meta["ok"] is True


def test_manifest_records_counts_and_hashes(tmp_path):
    src = _make_db(tmp_path / "src.db")
    records = tmp_path / "records"
    export_db_to_records(src, records)
    manifest = json.loads((records / "manifest.json").read_text())
    assert manifest["record_streams"]["persons"]["count"] == 2
    assert manifest["record_streams"]["positions"]["count"] == 2
    assert manifest["record_streams"]["persons"]["sha256"] == streams.jsonl_sha256(
        records / "persons.jsonl"
    )


def test_rebuild_is_rerunnable_and_consistent(tmp_path):
    src = _make_db(tmp_path / "src.db")
    records = tmp_path / "records"
    export_db_to_records(src, records)
    b1 = tmp_path / "b1.db"
    b2 = tmp_path / "b2.db"
    rebuild_db_from_records(records, b1, overwrite=True)
    rebuild_db_from_records(records, b2, overwrite=True)
    assert verify_consistency(records, b1)["consistent"]
    assert verify_consistency(records, b2)["consistent"]


def test_rebuild_refuses_existing_without_overwrite(tmp_path):
    src = _make_db(tmp_path / "src.db")
    records = tmp_path / "records"
    export_db_to_records(src, records)
    backup = tmp_path / "backup.db"
    rebuild_db_from_records(records, backup, overwrite=True)
    with pytest.raises(FileExistsError):
        rebuild_db_from_records(records, backup, overwrite=False)


def test_profile_flattening_is_idempotent_shape(tmp_path):
    """Generation flattens a person profile into canonical records."""
    from gov_relation.canon.pillar_build import profile_to_records

    profile = {
        "identity": {"person_id": "x_p1", "name": "王五"},
        "career_timeline": [{"org": "甲", "title": "书记", "start": "2020"}],
        "relationships": [{"type": "同事", "name": "人A"}],
    }
    r = profile_to_records(profile)
    assert r["persons"][0]["canonical_name"] == "王五"
    assert len(r["positions"]) == 1
    assert len(r["relationships"]) == 1