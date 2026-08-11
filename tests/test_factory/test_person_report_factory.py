"""Tests for person JSON and report generation."""

import sqlite3

from gov_relation.factory import (
    InsertFactory,
    PersonJSONFactory,
    ReportFactory,
    SchemaFactory,
)


def test_person_profile_satisfies_promotion_contract(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(conn)
    inserts = InsertFactory()
    person = inserts.upsert_person(
        conn, {"canonical_name": "张三", "birth_text": "1965"}
    )
    inserts.insert_position(
        conn,
        {
            "person_id": person,
            "title": "县委书记",
            "organization_text": "某县委",
            "is_current": 1,
        },
    )
    source = inserts.insert_source(
        conn, {"canonical_url": "https://example.test/a", "title": "任免通知"}
    )
    inserts.link_evidence(conn, source, "person", person, "canonical_name")
    profile = PersonJSONFactory().build(conn, person)
    assert profile["identity"]["name"] == "张三"
    assert profile["career_timeline"][0]["title"] == "县委书记"
    assert profile["source_register"][0]["title"] == "任免通知"


def test_report_uses_database_counts(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(conn)
    InsertFactory().upsert_person(
        conn, {"canonical_name": "张三", "birth_text": "1965"}
    )
    report = ReportFactory().build_from_conn(conn, "测试县")
    assert "# 测试县" in report
    assert "| 人员 | 1 |" in report
