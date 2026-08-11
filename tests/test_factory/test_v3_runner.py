"""Failure-safety and identity tests for the v3 runner backend."""

import sqlite3

import pytest

from gov_relation.factory import GEXFFactory
from gov_relation.runner import run_build


def _run(tmp_path, **overrides):
    arguments = {
        "slug": "测试县",
        "persons": [{"canonical_name": "甲", "birth_text": "1960"}],
        "organizations": [],
        "positions": [],
        "relationships": [],
        "db_path": tmp_path / "output.db",
        "gexf_path": tmp_path / "output.gexf",
        "backend": "v3",
        "overwrite": True,
    }
    arguments.update(overrides)
    run_build(**arguments)


def test_failed_graph_build_preserves_both_old_outputs(tmp_path, monkeypatch):
    database = tmp_path / "output.db"
    graph = tmp_path / "output.gexf"
    database.write_bytes(b"old database")
    graph.write_text("old graph", encoding="utf-8")

    def fail(*args, **kwargs):
        raise RuntimeError("graph failed")

    monkeypatch.setattr(GEXFFactory, "write", fail)
    with pytest.raises(RuntimeError, match="graph failed"):
        _run(tmp_path)

    assert database.read_bytes() == b"old database"
    assert graph.read_text(encoding="utf-8") == "old graph"
    assert not list(tmp_path.glob(".*.building"))


def test_unknown_birth_requires_stable_source_reference(tmp_path):
    with pytest.raises(ValueError, match="source_pk"):
        _run(tmp_path, persons=[{"canonical_name": "甲"}])
    assert not (tmp_path / "output.db").exists()
    assert not (tmp_path / "output.gexf").exists()


def test_ambiguous_name_reference_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="ambiguous person name"):
        _run(
            tmp_path,
            persons=[
                {"canonical_name": "同名", "_source_pk": "one"},
                {"canonical_name": "同名", "_source_pk": "two"},
            ],
            positions=[{"person_name": "同名", "title": "主任"}],
        )


def test_position_tenures_are_not_collapsed(tmp_path):
    _run(
        tmp_path,
        persons=[{"canonical_name": "甲", "_source_pk": "one"}],
        organizations=[{"canonical_name": "机构"}],
        positions=[
            {
                "person_ref": "one", "organization_name": "机构",
                "title": "主任", "start_text": "2010", "end_text": "2015",
            },
            {
                "person_ref": "one", "organization_name": "机构",
                "title": "主任", "start_text": "2016", "end_text": "2020",
            },
        ],
    )
    conn = sqlite3.connect(tmp_path / "output.db")
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 2
    conn.close()


def test_explicit_reference_resolves_duplicate_names(tmp_path):
    _run(
        tmp_path,
        persons=[
            {"canonical_name": "同名", "_source_pk": "one"},
            {"canonical_name": "同名", "_source_pk": "two"},
        ],
        positions=[{"person_ref": "one", "title": "主任"}],
    )
    conn = sqlite3.connect(tmp_path / "output.db")
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 1
    conn.close()


def test_person_ids_do_not_depend_on_input_order(tmp_path):
    people = [
        {"canonical_name": "甲", "_source_pk": "one"},
        {"canonical_name": "乙", "_source_pk": "two"},
    ]
    _run(tmp_path, persons=people)
    conn = sqlite3.connect(tmp_path / "output.db")
    first = dict(conn.execute("SELECT canonical_name, person_id FROM persons"))
    conn.close()
    _run(tmp_path, persons=list(reversed(people)))
    conn = sqlite3.connect(tmp_path / "output.db")
    second = dict(conn.execute("SELECT canonical_name, person_id FROM persons"))
    conn.close()
    assert first == second
