"""Tests for the canonical v2 data platform."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from gov_relation.platform.identity import person_key, stable_id
from gov_relation.platform.importer import import_legacy_database, import_person_profile
from gov_relation.platform.quality import database_report
from gov_relation.platform.resolution import build_person_candidates
from gov_relation.platform.schema import SCHEMA_VERSION, connect, create_schema


def _target(path: Path) -> sqlite3.Connection:
    conn = connect(path)
    create_schema(conn)
    return conn


def _legacy_database(path: Path) -> None:
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, birth TEXT, current_post TEXT,
            current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT, type TEXT);
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY, person_a_id INTEGER, person_b_id INTEGER,
            type TEXT, strongth TEXT, overlap_org TEXT, overlap_period TEXT
        );
        INSERT INTO persons VALUES
            (1, '张三', '1977-01', '县长', '测试县政府', 'https://example.gov/p/1'),
            (2, '李四', '', '副县长', '测试县政府', '公开资料');
        INSERT INTO organizations VALUES (10, '测试县政府', 'government');
        INSERT INTO positions VALUES (1, 1, 10, '县长', '2020', 'present');
        INSERT INTO relationships VALUES (1, 1, 2, 'overlap', 'strong', '10', '2020-present');
        """
    )
    conn.commit()
    conn.close()


def test_schema_creates_layered_tables_and_gold_views(tmp_path: Path) -> None:
    conn = _target(tmp_path / "canonical.db")
    assert conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == SCHEMA_VERSION
    names = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')")
    }
    assert {
        "raw_records", "persons", "sources", "evidence_links", "quality_issues",
        "rights_review_keys", "rights_manifests", "source_rights_decisions",
    } <= names
    assert {
        "gold_current_positions", "gold_relationship_edges", "gold_commercial_sources",
        "gold_commercial_persons", "gold_commercial_positions", "gold_commercial_relationships",
        "gold_commercial_claims",
    } <= names
    assert list(conn.execute("PRAGMA foreign_key_check")) == []
    conn.close()


def test_identity_does_not_merge_name_only_records() -> None:
    first, first_status = person_key(name="张三", birth="", dataset_key="a", source_pk=1)
    second, second_status = person_key(name="张三", birth="", dataset_key="b", source_pk=1)
    assert first != second
    assert first_status == second_status == "unresolved"
    verified_a, status_a = person_key(name="张三", birth="1977-01", dataset_key="a", source_pk=1)
    verified_b, status_b = person_key(name=" 张 三 ", birth="1977-01", dataset_key="b", source_pk=9)
    assert verified_a == verified_b
    assert status_a == status_b == "verified"
    approximate, approximate_status = person_key(
        name="张三", birth='1980年代（媒体称"80后"）', dataset_key="a", source_pk=1
    )
    assert approximate.startswith("scoped:")
    assert approximate_status == "unresolved"


def test_imports_legacy_schema_variants_losslessly(tmp_path: Path) -> None:
    legacy = tmp_path / "测试县_network.db"
    _legacy_database(legacy)
    conn = _target(tmp_path / "canonical.db")
    stats = import_legacy_database(conn, legacy, source_root=tmp_path)
    conn.commit()

    assert stats.persons == 2
    assert stats.organizations == 1
    assert stats.positions == 1
    assert stats.relationships == 1
    assert stats.raw_records == 5
    assert stats.jurisdictions == 1
    assert conn.execute("SELECT COUNT(*) FROM raw_records").fetchone()[0] == 5
    assert conn.execute("SELECT strength FROM relationships").fetchone()[0] == "strong"
    assert conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0] == 2
    assert list(conn.execute("PRAGMA foreign_key_check")) == []

    repeated = import_legacy_database(conn, legacy, source_root=tmp_path)
    assert repeated.skipped == 1
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 1
    conn.close()


def test_imports_profile_sources_timeline_and_claims(tmp_path: Path) -> None:
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": "2026-08-10",
                "investigation_scope": {"province": "测试省", "region": "测试县"},
                "identity": {"person_id": "p1", "name": "张三", "birth": "1977-01"},
                "current_status": {
                    "current_post": "县长", "current_org": "测试县政府",
                    "as_of": "2026-08-10", "is_current_confirmed": True,
                },
                "career_timeline": [
                    {
                        "start": "2020", "end": "present", "org": "测试县政府",
                        "title": "县长", "confidence": "confirmed", "source_ids": ["S001"],
                    }
                ],
                "governance_record": [{"domain": "education", "confidence": "plausible"}],
                "relationships": [
                    {
                        "person": "李四", "relationship_type": "overlap", "strength": "strong",
                        "confidence": "confirmed", "overlap_org": "测试县政府",
                        "overlap_period": "2020-present", "source_ids": ["S001"],
                    }
                ],
                "risk_and_integrity_signals": [],
                "open_questions": [{"question": "早期履历？"}],
                "source_register": [
                    {
                        "id": "S001", "url": "https://example.gov/p/1", "title": "领导简历",
                        "source_type": "official", "reliability": "high",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    conn = _target(tmp_path / "canonical.db")
    stats = import_person_profile(conn, profile_path, source_root=tmp_path)
    conn.commit()

    assert stats.profiles == 1
    assert stats.positions == 1
    assert stats.sources == 1
    assert stats.claims == 2
    assert stats.relationships == 1
    assert stats.jurisdictions == 2
    assert conn.execute("SELECT COUNT(*) FROM evidence_links").fetchone()[0] == 2
    report = database_report(conn)
    assert report["foreign_key_errors"] == []
    assert report["commercial_release_ready"] is False
    assert report["rights"]["commercially_exportable"]["positions"] == 0
    conn.close()


def test_stable_ids_are_deterministic() -> None:
    assert stable_id("per", "张三|1977") == stable_id("per", "张三|1977")


def test_resolution_requires_more_than_same_name(tmp_path: Path) -> None:
    conn = _target(tmp_path / "canonical.db")
    conn.executemany(
        """INSERT INTO persons
           (person_id, canonical_name, normalized_name, birthplace, identity_status)
           VALUES (?, '张三', '张三', ?, ?)""",
        [("p1", "测试县", "verified"), ("p2", "测试县", "unresolved"), ("p3", "另一县", "unresolved")],
    )
    created = build_person_candidates(conn)
    assert created == 1
    row = conn.execute(
        "SELECT left_entity_id, right_entity_id, score FROM resolution_candidates"
    ).fetchone()
    assert {row[0], row[1]} == {"p1", "p2"}
    assert row[2] >= 0.65
    conn.close()
