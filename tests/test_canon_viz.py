"""Regression checks for canonical graph serialization and edge selection."""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest

from gov_relation.canon.pillar_viz import _build_graph
from gov_relation.canon.streams import iter_jsonl, write_jsonl


NS = {"g": "http://www.gexf.net/1.2draft"}


def _save(root, kind, rows):
    write_jsonl(root / f"{kind}.jsonl", iter(rows))


def test_gexf_is_valid_and_matches_jsonl_index(tmp_path):
    records = tmp_path / "records"
    _save(records, "persons", [
        {"person_id": "p<&\"1", "canonical_name": "甲<&\"\u0001"},
        {"person_id": "p2", "canonical_name": "乙"},
    ])
    _save(records, "relationships", [
        {"person_from_id": "p<&\"1", "person_to_id": "p2", "relationship_type": "同事<&\"", "direction": "undirected"},
        {"person_from_id": "p<&\"1", "person_to_id": "p2", "relationship_type": "工作交集", "direction": "to_from"},
        {"person_from_id": "p2", "person_to_id": "p2", "relationship_type": "self"},
        {"person_from_id": "p2", "person_to_id": "missing", "relationship_type": "dangling"},
    ])
    stats = _build_graph(records, tmp_path / "out")
    assert stats == {"nodes": 2, "positions": 0, "edges": 2}
    xml = ET.parse(tmp_path / "out" / "graph" / "platform-graph.gexf")
    nodes = xml.findall(".//g:node", NS)
    edges = xml.findall(".//g:edge", NS)
    assert len(nodes) == 2
    assert nodes[0].attrib == {"id": 'p<&"1', "label": "甲<&\""}
    assert len(edges) == 2
    assert edges[0].attrib["type"] == "undirected"
    assert edges[0].attrib["label"] == '同事<&"'
    assert (edges[1].attrib["source"], edges[1].attrib["target"]) == ("p2", 'p<&"1')
    assert edges[1].attrib["type"] == "directed"
    index_rows = list(iter_jsonl(tmp_path / "out" / "graph" / "platform-index.jsonl"))
    assert len(index_rows) == 4
    assert [row["source"] for row in index_rows[2:]] == [e.attrib["source"] for e in edges]
    assert [row["target"] for row in index_rows[2:]] == [e.attrib["target"] for e in edges]
    assert [row["type"] for row in index_rows[2:]] == [e.attrib["label"] for e in edges]


def test_unknown_direction_does_not_publish_graph(tmp_path):
    records = tmp_path / "records"
    _save(records, "persons", [{"person_id": "p1"}, {"person_id": "p2"}])
    _save(records, "relationships", [{"person_from_id": "p1", "person_to_id": "p2", "direction": "sideways"}])
    with pytest.raises(ValueError, match="direction"):
        _build_graph(records, tmp_path / "out")
    assert not (tmp_path / "out" / "graph" / "platform-graph.gexf").exists()


def test_duplicate_person_id_with_conflicting_profile_is_rejected(tmp_path):
    records = tmp_path / "records"
    _save(records, "persons", [{"person_id": "p1", "canonical_name": "甲"}, {"person_id": "p1", "canonical_name": "乙"}])
    with pytest.raises(ValueError, match="Conflicting person"):
        _build_graph(records, tmp_path / "out")
