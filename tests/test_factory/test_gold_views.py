"""Semantic tests for gold_current_positions (spec §4.5, implemented view)."""

import sqlite3

import pytest

from gov_relation.factory import InsertFactory, SchemaFactory


@pytest.fixture
def conn(tmp_path):
    connection = sqlite3.connect(tmp_path / "gold.db")
    SchemaFactory().create_all(connection)
    return connection


def _seed(conn):
    factory = InsertFactory()
    current = factory.upsert_person(
        conn, {"canonical_name": "张明", "birth_text": "1968-06"}
    )
    former = factory.upsert_person(
        conn, {"canonical_name": "李强", "birth_text": "1955-11"}
    )
    org = factory.upsert_organization(conn, {"canonical_name": "某市人民政府"})
    factory.insert_position(
        conn,
        {
            "person_id": current,
            "organization_id": org,
            "organization_text": "某市人民政府",
            "title": "市长",
            "rank": "正厅级",
            "start_text": "2021-02",
            "is_current": 1,
        },
    )
    factory.insert_position(
        conn,
        {
            "person_id": former,
            "organization_id": org,
            "organization_text": "某市人民政府",
            "title": "市长",
            "start_text": "2016-03",
            "end_text": "2021-01",
            "is_current": 0,
        },
    )
    return current, former


def test_gold_view_lists_only_current_positions(conn):
    current, former = _seed(conn)
    rows = conn.execute(
        "SELECT person_id, canonical_name, title, organization_name, "
        "start_text, end_text FROM gold_current_positions"
    ).fetchall()
    assert len(rows) == 1
    person_id, name, title, org_name, start, end = rows[0]
    assert person_id == current
    assert person_id != former
    assert name == "张明"
    assert title == "市长"
    assert org_name == "某市人民政府"
    assert start == "2021-02"
    assert end == ""


def test_gold_view_left_joins_organization(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "王芳", "birth_text": "1970-01"}
    )
    factory.insert_position(
        conn,
        {
            "person_id": person,
            "title": "县委书记",
            "start_text": "2022-05",
            "is_current": 1,
        },
    )
    rows = conn.execute(
        "SELECT canonical_name, organization_name FROM gold_current_positions"
    ).fetchall()
    assert len(rows) == 1
    assert rows[0][0] == "王芳"
    assert rows[0][1] is None