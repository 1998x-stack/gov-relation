"""Schema and identity safety for canonical profile ingestion."""

from __future__ import annotations

import json

import pytest

from gov_relation.canon.pillar_build import _append_idempotent, profile_to_records
from gov_relation.canon.streams import iter_jsonl


def test_profile_enums_and_boolean_fields_are_schema_compatible():
    records = profile_to_records({
        "identity": {"person_id": "p1", "name": "甲", "identity_status": "complete"},
        "career_timeline": [{"title": "职务", "confidence": "", "date_precision": "", "is_current": "false"}],
        "relationships": [{"person_id": "p2", "type": "共事", "confidence": "", "direction": "", "strength": ""}],
    })
    person = records["persons"][0]
    assert person["identity_status"] == "unresolved"
    assert person["normalized_name"] == "甲"
    assert person["birth_precision"] == "unknown"
    position = records["positions"][0]
    assert position["date_precision"] == "unknown"
    assert position["confidence"] == "unverified"
    assert position["is_current"] == 0
    relationship = records["relationships"][0]
    assert relationship["person_to_id"] == "p2"
    assert relationship["direction"] == "undirected"
    assert relationship["strength"] == "unknown"
    assert relationship["confidence"] == "unverified"


def test_name_only_candidate_is_not_exported_as_an_entity_edge():
    records = profile_to_records({
        "identity": {"person_id": "p1", "name": "甲"},
        "relationships": [{"name": "同名待核实", "type": "共事"}],
    })
    assert records["relationships"] == []
    claim = records["claims"][0]
    assert claim["subject_id"] == "p1"
    assert claim["confidence"] == "unverified"
    assert claim["review_status"] == "pending"
    assert json.loads(claim["value_json"])["name"] == "同名待核实"


def test_append_is_idempotent_within_batch_and_rejects_changed_existing_id(tmp_path):
    target = tmp_path / "persons.jsonl"
    row = {"person_id": "p1", "canonical_name": "甲"}
    assert _append_idempotent(target, "persons", [row, row]) == 1
    assert _append_idempotent(target, "persons", [row]) == 0
    with pytest.raises(ValueError, match="Conflicting persons record"):
        _append_idempotent(target, "persons", [{"person_id": "p1", "canonical_name": "乙"}])
    assert list(iter_jsonl(target)) == [row]


def test_self_link_does_not_become_a_relationship_edge():
    with pytest.raises(ValueError, match="Self relationship"):
        profile_to_records({
            "identity": {"person_id": "p1"},
            "relationships": [{"person_id": "p1", "type": "same"}],
        })
