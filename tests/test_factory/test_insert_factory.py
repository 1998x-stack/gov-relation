"""Tests for deterministic v3 inserts."""

import json
import sqlite3

import pytest

from gov_relation.factory import InsertFactory, SchemaFactory


@pytest.fixture
def conn(tmp_path):
    connection = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(connection)
    return connection


def test_person_upsert_is_idempotent(conn):
    factory = InsertFactory()
    data = {"canonical_name": "张三", "birth_text": "1965-03"}
    assert factory.upsert_person(conn, data) == factory.upsert_person(conn, data)
    assert conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0] == 1


def test_unscoped_person_without_birth_is_rejected(conn):
    with pytest.raises(ValueError, match="source_pk"):
        InsertFactory().upsert_person(conn, {"canonical_name": "同名"})


def test_same_name_without_birth_stays_distinct_by_source_pk(conn):
    factory = InsertFactory()
    a = factory.upsert_person(conn, {"canonical_name": "同名"}, source_pk="row-1")
    b = factory.upsert_person(conn, {"canonical_name": "同名"}, source_pk="row-2")
    assert a != b


def test_position_ids_include_person_and_start(conn):
    factory = InsertFactory()
    a = factory.upsert_person(conn, {"canonical_name": "A", "birth_text": "1960"})
    b = factory.upsert_person(conn, {"canonical_name": "B", "birth_text": "1965"})
    first = factory.insert_position(
        conn, {"person_id": a, "title": "县委书记", "start_text": "2020-01"}
    )
    second = factory.insert_position(
        conn, {"person_id": b, "title": "县委书记", "start_text": "2021-01"}
    )
    assert first != second


def test_position_ids_include_organization(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "A", "birth_text": "1960"}
    )
    first_org = factory.upsert_organization(
        conn, {"canonical_name": "机构一"}
    )
    second_org = factory.upsert_organization(
        conn, {"canonical_name": "机构二"}
    )
    first = factory.insert_position(
        conn,
        {
            "person_id": person, "organization_id": first_org,
            "title": "书记", "start_text": "2020",
        },
    )
    second = factory.insert_position(
        conn,
        {
            "person_id": person, "organization_id": second_org,
            "title": "书记", "start_text": "2020",
        },
    )
    assert first != second


def test_distinct_position_tenures_get_distinct_ids(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "P", "birth_text": "1960"}
    )
    org = factory.upsert_organization(conn, {"canonical_name": "机构"})
    first = factory.insert_position(
        conn,
        {
            "person_id": person, "organization_id": org,
            "title": "书记", "start_text": "2010", "end_text": "2015",
        },
    )
    second = factory.insert_position(
        conn,
        {
            "person_id": person, "organization_id": org,
            "title": "书记", "start_text": "2016", "end_text": "2020",
        },
    )
    assert first != second
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 2


def test_position_ids_include_tenure_end_and_current(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "P", "birth_text": "1960"}
    )
    org = factory.upsert_organization(conn, {"canonical_name": "机构"})
    ended = factory.insert_position(
        conn,
        {
            "person_id": person, "organization_id": org,
            "title": "书记", "start_text": "2010", "end_text": "2015",
        },
    )
    ongoing = factory.insert_position(
        conn,
        {
            "person_id": person, "organization_id": org,
            "title": "书记", "start_text": "2010", "end_text": "present",
            "is_current": 1,
        },
    )
    assert ended != ongoing
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 2


def test_identical_position_tenure_is_idempotent(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "P", "birth_text": "1960"}
    )
    org = factory.upsert_organization(conn, {"canonical_name": "机构"})
    data = {
        "person_id": person, "organization_id": org,
        "title": "书记", "start_text": "2010", "end_text": "2015",
        "is_current": 0,
    }
    assert factory.insert_position(conn, data) == factory.insert_position(
        conn, data
    )
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 1


def test_relationship_ids_include_type(conn):
    factory = InsertFactory()
    a = factory.upsert_person(conn, {"canonical_name": "A", "birth_text": "1960"})
    b = factory.upsert_person(conn, {"canonical_name": "B", "birth_text": "1965"})
    coworker = factory.insert_relationship(
        conn,
        {"person_from_id": a, "person_to_id": b, "relationship_type": "coworker"},
    )
    family = factory.insert_relationship(
        conn,
        {"person_from_id": a, "person_to_id": b, "relationship_type": "family"},
    )
    assert coworker != family


def test_relationship_ids_include_episode_context(conn):
    factory = InsertFactory()
    person_a = factory.upsert_person(
        conn, {"canonical_name": "A", "birth_text": "1960"}
    )
    person_b = factory.upsert_person(
        conn, {"canonical_name": "B", "birth_text": "1961"}
    )
    first = factory.insert_relationship(
        conn,
        {
            "person_from_id": person_a, "person_to_id": person_b,
            "relationship_type": "coworker", "overlap_period_text": "2020",
        },
    )
    second = factory.insert_relationship(
        conn,
        {
            "person_from_id": person_a, "person_to_id": person_b,
            "relationship_type": "coworker", "overlap_period_text": "2021",
        },
    )
    assert first != second


def test_invalid_relationship_direction_is_not_silently_ignored(conn):
    factory = InsertFactory()
    person_a = factory.upsert_person(
        conn, {"canonical_name": "A", "birth_text": "1960"}
    )
    person_b = factory.upsert_person(
        conn, {"canonical_name": "B", "birth_text": "1961"}
    )

    with pytest.raises(sqlite3.IntegrityError, match="CHECK constraint failed"):
        factory.insert_relationship(
            conn,
            {
                "person_from_id": person_a,
                "person_to_id": person_b,
                "relationship_type": "predecessor_successor",
                "direction": "invalid",
            },
        )


def test_source_claim_and_evidence_round_trip(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "C", "birth_text": "1970"}
    )
    source = factory.insert_source(
        conn, {"canonical_url": "https://example.test/source", "title": "通知"}
    )
    claim = factory.insert_claim(
        conn,
        {
            "subject_type": "person",
            "subject_id": person,
            "predicate": "current_post",
            "value": "县长",
        },
    )
    evidence = factory.link_evidence(
        conn, source, "claim", claim, "value", "paragraph-1"
    )
    stored = conn.execute(
        "SELECT value_json FROM claims WHERE claim_id=?", (claim,)
    ).fetchone()[0]
    assert stored == "县长"
    assert conn.execute(
        "SELECT 1 FROM evidence_links WHERE evidence_id=?", (evidence,)
    ).fetchone()


def test_claim_string_value_is_stored_raw(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "C", "birth_text": "1970"}
    )
    claim = factory.insert_claim(
        conn,
        {
            "subject_type": "person",
            "subject_id": person,
            "predicate": "current_post",
            "value": "县长",
        },
    )
    stored = conn.execute(
        "SELECT value_json FROM claims WHERE claim_id=?", (claim,)
    ).fetchone()[0]
    assert stored == "县长"


def test_claim_non_string_value_is_stored_as_json(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "C", "birth_text": "1970"}
    )
    claim = factory.insert_claim(
        conn,
        {
            "subject_type": "person",
            "subject_id": person,
            "predicate": "governance_record",
            "value": {"domain": "education", "since": 2020},
        },
    )
    stored = conn.execute(
        "SELECT value_json FROM claims WHERE claim_id=?", (claim,)
    ).fetchone()[0]
    assert json.loads(stored) == {"domain": "education", "since": 2020}


def test_claim_value_json_is_not_double_encoded(conn):
    factory = InsertFactory()
    person = factory.upsert_person(
        conn, {"canonical_name": "C", "birth_text": "1970"}
    )
    payload = json.dumps(
        {"domain": "教育", "since": 2020},
        ensure_ascii=False,
        sort_keys=True,
    )
    claim = factory.insert_claim(
        conn,
        {
            "subject_type": "person",
            "subject_id": person,
            "predicate": "governance_record",
            "value_json": payload,
        },
    )
    stored = conn.execute(
        "SELECT value_json FROM claims WHERE claim_id=?", (claim,)
    ).fetchone()[0]
    assert stored == payload
