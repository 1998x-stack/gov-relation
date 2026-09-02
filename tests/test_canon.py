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

def test_region_partition_namespacing(tmp_path):
    """Region build produces canonical per-type JSONL with scoped ids."""
    from gov_relation.canon.pillar_region import region_records, write_region

    rec = region_records(
        "某县",
        persons=[{"id": 1, "name": "张三", "gender": "男"}],
        organizations=[{"id": 10, "name": "某县委", "type": "party"}],
        positions=[{"person_id": 1, "org_id": 10, "title": "书记"}],
        relationships=[{"person_a": 1, "person_b": 99, "type": "前后任"}],
    )
    assert rec["persons"][0]["person_id"] == "某县:person:1"
    assert rec["persons"][0]["canonical_name"] == "张三"
    assert rec["positions"][0]["person_id"] == "某县:person:1"
    assert rec["relationships"][0]["person_from_id"] == "某县:person:1"

    pdir = write_region(tmp_path, "某县", "测试省", rec)
    assert (pdir / "persons.jsonl").exists()
    assert (pdir / "organizations.jsonl").exists()
    assert (pdir / ".meta.json").exists()


def test_snapshot_aggregation_idempotent(tmp_path):
    """gov2 snapshot merges partitioned regions into unified streams once."""
    from gov_relation.canon.pillar_region import (
        region_records,
        snapshot_regions,
        write_region,
    )

    root = tmp_path / "records"
    rec = region_records(
        "临江",
        persons=[{"id": 1, "name": "李雷"}],
        organizations=[],
        positions=[],
        relationships=[],
    )
    write_region(root, "临江", "江苏省", rec)
    assert snapshot_regions(root)["persons"] == 1
    # idempotent: second run adds 0
    assert snapshot_regions(root)["persons"] == 0
    from gov_relation.canon.streams import iter_jsonl

    assert sum(1 for _ in iter_jsonl(root / "persons.jsonl")) == 1


def test_region_records_emit_schema_valid_enums():
    """Region rows must satisfy the platform CHECK enums when loaded into SQLite."""
    from gov_relation.canon.pillar_region import region_records

    rec = region_records(
        "测试区",
        persons=[{"id": 1, "name": "A"}],
        organizations=[{"id": 1, "name": "X"}],
        positions=[{"person_id": 1, "org_id": 1, "title": "书记"}],
        relationships=[{"person_a": 1, "person_b": 2, "type": "同事"}],
    )
    p = rec["persons"][0]
    assert p["identity_status"] in {"verified", "probable", "unresolved", "merged"}
    assert p["birth_precision"] in {"day", "month", "year", "unknown"}
    pos = rec["positions"][0]
    assert pos["date_precision"] in {"day", "month", "year", "range", "unknown"}
    assert pos["confidence"] in {"confirmed", "plausible", "unverified"}
    rel = rec["relationships"][0]
    assert rel["direction"] in {"undirected", "from_to", "to_from"}
    assert rel["strength"] in {"strong", "medium", "weak", "unknown"}
