"""Pillar B — 数据可视化 (data visualization).

Reads the canonical JSONL (/ the SQLite backup) and emits visual artefacts:
a GEXF relationship graph and a lightweight node/edge summary. The SQLite
backup path is only used for fast traversal; the authoritative source is JSONL.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .streams import iter_jsonl


def _load(records_dir: Path, kind: str) -> list[dict]:
    path = records_dir / f"{kind}.jsonl"
    if path.exists():
        return list(iter_jsonl(path))
    return []


def _build_graph(records_dir: Path, out_dir: Path) -> dict:
    out_dir = out_dir / "graph"
    out_dir.mkdir(parents=True, exist_ok=True)

    persons = _load(records_dir, "persons")
    positions = _load(records_dir, "positions")
    relationships = _load(records_dir, "relationships")

    person_by_id = {p["person_id"]: p for p in persons}
    name_by_id = {pid: p.get("canonical_name", pid) for pid, p in person_by_id.items()}

    # GEXF
    gexf_path = out_dir / "platform-graph.gexf"
    with open(gexf_path, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0"?><gexf xmlns="http://www.gexf.net/1.2draft" version="1.2"><graph defaultedgetype="undirected"><nodes>')
        for pid, p in person_by_id.items():
            fh.write(f'<node id="{_esc(pid)}" label="{_esc(p.get("canonical_name",""))}"><attvalues/></node>')
        fh.write("</nodes><edges>")
        edge_id = 0
        for r in relationships:
            f = str(r.get("person_from_id", ""))
            t = str(r.get("person_to_id", ""))
            if f == t or f not in person_by_id or t not in person_by_id:
                continue
            fh.write(
                f'<edge id="{edge_id}" source="{_esc(f)}" target="{_esc(t)}" type="{_esc(r.get("relationship_type",""))}"/>'
            )
            edge_id += 1
        fh.write("</edges></graph></gexf>")

    # node/edge index jsonl (canonical-grade, sortable)
    idx = out_dir / "platform-index.jsonl"
    nodes = [{"kind": "person", "id": pid, "name": name_by_id.get(pid, "")} for pid in person_by_id]
    edges = [
        {
            "source": str(r.get("person_from_id", "")),
            "target": str(r.get("person_to_id", "")),
            "type": r.get("relationship_type", ""),
        }
        for r in relationships
        if str(r.get("person_from_id")) != str(r.get("person_to_id"))
    ]
    with open(idx, "w", encoding="utf-8") as fh:
        for n in nodes:
            fh.write(json.dumps(n, ensure_ascii=False, sort_keys=True))
            fh.write("\n")
        for e in edges:
            fh.write(json.dumps(e, ensure_ascii=False, sort_keys=True))
            fh.write("\n")
    return {"nodes": len(person_by_id), "positions": len(positions), "edges": len(edges)}


def _esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pillar_viz(args) -> int:
    import json as _json
    from gov_relation.paths import DATA_DIR

    records_dir = Path(args.records)
    out_dir = DATA_DIR
    stats = _build_graph(records_dir, out_dir)
    print(_json.dumps(stats, ensure_ascii=False))
    return 0