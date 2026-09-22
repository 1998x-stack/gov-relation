"""Pillar B: render a canonical person relationship graph and matching index.

Only relationships whose two endpoints are known people are exported. GEXF
edge ``type`` is reserved for the graph direction; the domain relationship
kind is recorded as the edge label instead.
"""

from __future__ import annotations

import json
import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from .streams import iter_jsonl, write_jsonl


def _load(records_dir: Path, kind: str) -> list[dict]:
    path = records_dir / f"{kind}.jsonl"
    return list(iter_jsonl(path)) if path.exists() else []


def _xml_text(value: object) -> str:
    """Remove characters forbidden by XML 1.0 without changing source data."""
    return "".join(
        ch for ch in str(value if value is not None else "")
        if ch in "\t\n\r" or (" " <= ch <= "\ud7ff")
        or ("\ue000" <= ch <= "\ufffd")
        or ("\U00010000" <= ch <= "\U0010ffff")
    )


def _graph_edges(relationships: list[dict], known_people: set[str]) -> list[dict]:
    """Resolve both graph and index edges using exactly the same rules."""
    edges = []
    for relationship in relationships:
        source = relationship.get("person_from_id")
        target = relationship.get("person_to_id")
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        if not source or not target or source == target:
            continue
        if source not in known_people or target not in known_people:
            continue
        direction = relationship.get("direction") or "undirected"
        if direction not in {"undirected", "from_to", "to_from"}:
            raise ValueError(f"Unrecognized relationship direction: {direction!r}")
        if direction == "to_from":
            source, target = target, source
        edges.append({
            "source": source,
            "target": target,
            "type": relationship.get("relationship_type") or "",
            "direction": "undirected" if direction == "undirected" else "directed",
        })
    return edges


def _build_graph(records_dir: Path, out_dir: Path) -> dict:
    out_dir = out_dir / "graph"
    out_dir.mkdir(parents=True, exist_ok=True)

    persons = _load(records_dir, "persons")
    positions = _load(records_dir, "positions")
    relationships = _load(records_dir, "relationships")

    person_by_id: dict[str, dict] = {}
    for person in persons:
        person_id = person.get("person_id")
        if not isinstance(person_id, str) or not person_id:
            raise ValueError("A graph person is missing a nonempty person_id")
        if person_id in person_by_id and person_by_id[person_id] != person:
            raise ValueError(f"Conflicting person records for {person_id!r}")
        person_by_id[person_id] = person
    edges = _graph_edges(relationships, set(person_by_id))

    root = ET.Element("gexf", {"xmlns": "http://www.gexf.net/1.2draft", "version": "1.2"})
    graph = ET.SubElement(root, "graph", {"mode": "static", "defaultedgetype": "undirected"})
    graph_nodes = ET.SubElement(graph, "nodes")
    for person_id, person in person_by_id.items():
        ET.SubElement(graph_nodes, "node", {
            "id": _xml_text(person_id),
            "label": _xml_text(person.get("canonical_name") or person_id),
        })
    graph_edges = ET.SubElement(graph, "edges")
    for edge_id, edge in enumerate(edges):
        ET.SubElement(graph_edges, "edge", {
            "id": str(edge_id),
            "source": _xml_text(edge["source"]),
            "target": _xml_text(edge["target"]),
            "type": edge["direction"],
            "label": _xml_text(edge["type"]),
        })

    gexf_path = out_dir / "platform-graph.gexf"
    fd, tmp_name = tempfile.mkstemp(prefix=".platform-graph-", suffix=".gexf", dir=out_dir)
    try:
        with os.fdopen(fd, "wb") as file:
            ET.ElementTree(root).write(file, encoding="utf-8", xml_declaration=True)
        os.replace(tmp_name, gexf_path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise

    nodes = [
        {"kind": "person", "id": pid, "name": p.get("canonical_name") or pid}
        for pid, p in person_by_id.items()
    ]
    write_jsonl(out_dir / "platform-index.jsonl", iter([*nodes, *edges]))
    return {"nodes": len(person_by_id), "positions": len(positions), "edges": len(edges)}


def pillar_viz(args) -> int:
    from gov_relation.paths import DATA_DIR

    stats = _build_graph(Path(args.records), DATA_DIR)
    print(json.dumps(stats, ensure_ascii=False))
    return 0
