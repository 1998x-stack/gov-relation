"""Tests for complete and stable GEXF rendering."""

import sqlite3
from xml.etree import ElementTree as ET

from gov_relation.factory import GEXFFactory, InsertFactory, SchemaFactory


def test_gexf_contains_title_attributes_and_stable_ids(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(conn)
    inserts = InsertFactory()
    first = inserts.upsert_person(
        conn, {"canonical_name": "甲", "birth_text": "1960"}
    )
    second = inserts.upsert_person(
        conn, {"canonical_name": "乙", "birth_text": "1965"}
    )
    inserts.insert_relationship(
        conn,
        {
            "person_from_id": first,
            "person_to_id": second,
            "relationship_type": "coworker",
            "context": "同期任职",
        },
    )
    xml = GEXFFactory().build(conn, "测试图")
    root = ET.fromstring(xml)
    assert root.tag == "{http://www.gexf.net/1.3}gexf"
    assert "测试图" in xml
    assert "coworker" in xml
    assert "同期任职" in xml
    assert f"person:{first}" in xml


def test_empty_database_is_valid_and_keeps_title(tmp_path):
    conn = sqlite3.connect(tmp_path / "factory.db")
    SchemaFactory().create_all(conn)
    xml = GEXFFactory().build(conn, "空图")
    ET.fromstring(xml)
    assert "空图" in xml
