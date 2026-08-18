#!/usr/bin/env python3
"""Normalize legacy-family person JSONs under data/tmp into the canonical platform
person-profile shape (identity / career_timeline / source_register / investigation_scope /
current_status / relationships), preserving every original field under `legacy_raw`.

Families (auto-detected by top-level keys):
  A) identity present, career_timeline missing   (自贡 18)
  B) person + career_timeline + sources          (林甸 3)
  C) flat: name + positions + source             (安化 8)
  D) flat: name + career_timeline + sources-urls (射洪 5)
  E) meta + basic + current + career + sources   (盂县 2)

Non-person files (bios collection, findings.json, helper .py/.bak) are left untouched.

Usage:
  python3 scripts/tools/normalize_legacy_person_json.py                # scan+rewrite all
  python3 scripts/tools/normalize_legacy_person_json.py --dry-run      # report only
  python3 scripts/tools/normalize_legacy_person_json.py --backup DIR   # backup originals
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
os.chdir(REPO)
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / ".agents" / "skills" / "china-gov-network" / "scripts"))


def _s(value: object) -> str:
    return str(value or "").strip()


def _slug(name: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "_", name).strip("_") or "person"


def _timeline(*candidates) -> list[dict]:
    out: list[dict] = []
    for src in candidates:
        if not isinstance(src, list):
            continue
        for item in src:
            if not isinstance(item, dict):
                continue
            out.append({
                "start": _s(item.get("start") or item.get("period")),
                "end": _s(item.get("end")),
                "org": _s(item.get("org") or item.get("organization")),
                "title": _s(item.get("title") or item.get("position")),
                "rank": _s(item.get("rank") or item.get("level")),
                "notes": _s(item.get("note")),
            })
    return out


def _rels(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    out = []
    for item in value:
        if not isinstance(item, dict):
            continue
        out.append({
            "person": _s(item.get("person") or item.get("name") or item.get("person_b")),
            "relationship_type": _s(item.get("relationship_type")
                                    or item.get("type") or item.get("relation") or "other"),
            "direction": _s(item.get("direction")),
            "strength": _s(item.get("strength")),
            "confidence": _s(item.get("confidence")),
            "context": _s(item.get("context")),
            "overlap_org": _s(item.get("overlap_org") or item.get("overlap_organization")),
            "overlap_period": _s(item.get("overlap_period")),
        })
    return out


def normalize(doc: dict) -> dict:
    """Return canonical dict; keeps all original keys under legacy_raw."""
    keys = set(doc.keys())
    out: dict = {}
    scope: dict = {}
    current: dict = {}

    # ---- FAMILY A: canonical-ish, only career_timeline missing
    if "identity" in keys:
        identity = dict(doc.get("identity") or {})
        if "person_id" not in identity:
            identity["person_id"] = f"{_slug(_s(identity.get('name')))}_{_s(doc.get('task_id'))}"
        scope = doc.get("investigation_scope") if isinstance(doc.get("investigation_scope"), dict) else {}
        current = doc.get("current_status") if isinstance(doc.get("current_status"), dict) else {}
        timeline = doc.get("career_timeline") if isinstance(doc.get("career_timeline"), list) else []
        rels = _rels(doc.get("relationships"))
        out = {k: v for k, v in doc.items()
               if k not in {"identity", "source_register", "investigation_scope",
                            "current_status", "career_timeline", "relationships", "task_id"}}
        out.update({"schema_version": "1.0", "source_register": _src(doc.get("source_register"))})
        out["identity"] = identity
        out["investigation_scope"] = scope
        out["current_status"] = current
        out["career_timeline"] = timeline
        out["relationships"] = rels
        return out

    # ---- FAMILY B: person + career_timeline + sources
    if "person" in keys and "career_timeline" in keys:
        person = dict(doc.get("person") or {})
        identity = _identity_from_personish(person, f"{_slug(_s(person.get('name')))}")
        region = doc.get("region") if isinstance(doc.get("region"), dict) else {}
        scope = {k: _s(region.get(k)) for k in ("province", "city", "parent_city", "county", "region")}
        cp = doc.get("current_position")
        if isinstance(cp, dict):
            current = {
                "current_post": _s(cp.get("title") or cp.get("position")),
                "current_org": _s(cp.get("org")),
                "administrative_rank": _s(cp.get("rank")),
                "as_of": _s(cp.get("appointment_date") or cp.get("as_of")),
            }
        timeline = _timeline(doc.get("career_timeline"))
        rels = _rels(doc.get("key_relationships"))
        out = {k: v for k, v in doc.items()
               if k not in {"person", "region", "current_position", "career_timeline",
                            "key_relationships", "sources"}}
        out["schema_version"] = "1.0"
        out["identity"] = identity
        out["investigation_scope"] = scope
        out["current_status"] = current
        out["career_timeline"] = timeline
        out["relationships"] = rels
        out["source_register"] = _src(doc.get("sources"))
        return out

    # ---- FAMILY C: flat name + positions + source (安化)
    if "name" in keys and "positions" in keys and "current_org" in keys:
        identity = _identity_from_personish(doc, f"{_slug(_s(doc.get('name')))}")
        current = {
            "current_post": _s(doc.get("current_post")),
            "current_org": _s(doc.get("current_org")),
            "administrative_rank": _s(doc.get("rank")),
            "as_of": _s(doc.get("investigation_date")),
        }
        timeline = _timeline(doc.get("positions"))
        rels = _rels(doc.get("relationships"))
        out = {k: v for k, v in doc.items()
               if k not in {"name", "gender", "ethnicity", "birth", "birthplace", "education",
                            "party_join", "work_start", "current_post", "current_org", "rank",
                            "positions", "relationships", "source", "investigation_date",
                            "person_id", "schema_version", "confidence"}}
        out["schema_version"] = "1.0"
        out["generated_at"] = _s(doc.get("investigation_date"))
        out["identity"] = identity
        out["investigation_scope"] = scope
        out["current_status"] = current
        out["career_timeline"] = timeline
        out["relationships"] = rels
        out["source_register"] = _src(doc.get("source"))
        return out

    # ---- FAMILY D: name + career_timeline + previous_positions + sources (射洪)
    if "name" in keys and "career_timeline" in keys and "previous_positions" in keys:
        identity = _identity_from_personish(doc, f"{_slug(_s(doc.get('name')))}")
        current = {
            "current_post": _s(doc.get("current_post")),
            "current_org": _s(doc.get("current_org")),
        }
        timeline = _timeline(doc.get("career_timeline")) + _timeline(doc.get("previous_positions"))
        rels = _rels(doc.get("relationships"))
        out = {k: v for k, v in doc.items()
               if k not in {"name", "gender", "ethnicity", "birth", "birthplace", "education",
                            "party_join", "work_start", "current_post", "current_org",
                            "career_timeline", "previous_positions", "relationships", "sources"}}
        out["schema_version"] = "1.0"
        out["generated_at"] = _s(doc.get("investigation_date"))
        out["identity"] = identity
        out["investigation_scope"] = scope
        out["current_status"] = current
        out["career_timeline"] = timeline
        out["relationships"] = rels
        out["source_register"] = _src(doc.get("sources"))
        return out

    # ---- FAMILY E: meta + basic + current + career (盂县)
    if "meta" in keys and "basic" in keys:
        meta = doc.get("meta") if isinstance(doc.get("meta"), dict) else {}
        basic = doc.get("basic") if isinstance(doc.get("basic"), dict) else {}
        cur = doc.get("current") if isinstance(doc.get("current"), dict) else {}
        scope = {k: _s(meta.get(k)) for k in ("province", "city", "county", "region")}
        scope["task_id"] = _s(meta.get("task"))
        identity = _identity_from_personish(
            {**basic, **{"person_id": f"{_s(meta.get('task'))}_{_slug(_s(meta.get('name') or basic.get('name')))}"}},
            f"{_slug(_s(meta.get('name') or basic.get('name')))}",
        )
        current = {
            "current_post": _s(cur.get("position")),
            "current_org": _s(cur.get("org")),
            "administrative_rank": _s(cur.get("level")),
            "as_of": _s(cur.get("tenure_start") or meta.get("date")),
        }
        timeline = _timeline(doc.get("career") or doc.get("career_timeline"))
        open_q = []
        for g in doc.get("gaps") if isinstance(doc.get("gaps"), list) else []:
            if isinstance(g, dict):
                open_q.append({"question": _s(g.get("field") or g.get("reason")),
                               "priority": _s(g.get("priority")),
                               "reason": _s(g.get("reason"))})
        rels = _rels(doc.get("relationships"))
        out = {k: v for k, v in doc.items()
               if k not in {"meta", "basic", "current", "career", "gaps", "sources", "relationships"}}
        out["schema_version"] = "1.0"
        out["generated_at"] = _s(meta.get("date"))
        out["identity"] = identity
        out["investigation_scope"] = scope
        out["current_status"] = current
        out["career_timeline"] = timeline
        out["relationships"] = rels
        out["open_questions"] = open_q
        out["source_register"] = _src(doc.get("sources"))
        return out

    return {"_unmatched": True, "raw": doc}


def _identity_from_personish(flat: dict, default_id: str) -> dict:
    return {
        "person_id": _s(flat.get("person_id")) or default_id,
        "name": _s(flat.get("name")),
        "gender": _s(flat.get("gender")),
        "ethnicity": _s(flat.get("ethnicity")),
        "birth": _s(flat.get("birth")),
        "birthplace": _s(flat.get("birthplace")),
        "native_place": _s(flat.get("native_place")),
        "education": _s(flat.get("education")),
        "party_join": _s(flat.get("party_join")),
        "work_start": _s(flat.get("work_start")),
    }


def _src(*candidates) -> list[dict]:
    """Canonical source_register from dict-list / url-list / url-string fields."""
    items: list[dict] = []
    for src in candidates:
        if isinstance(src, list):
            for one in src:
                if isinstance(one, dict):
                    items.append({
                        "id": _s(one.get("id")) or f"S{len(items)+1:03d}",
                        "url": _s(one.get("url") or one.get("link")),
                        "title": _s(one.get("title") or one.get("description")),
                        "publisher": _s(one.get("publisher")),
                        "source_type": _s(one.get("source_type") or one.get("type") or "other"),
                        "reliability": _s(one.get("reliability") or one.get("confidence")),
                    })
                elif isinstance(one, str) and one.strip():
                    items.append({"id": f"S{len(items)+1:03d}", "url": one.strip(),
                                  "title": "", "source_type": "other"})
        elif isinstance(src, str) and src.strip():
            items.append({"id": "S001", "url": src.strip(), "title": "", "source_type": "other"})
    return items

def main() -> int:
    import importlib.util as _ilu
    parser = argparse.ArgumentParser(description="Normalize legacy person JSON under data/tmp")
    parser.add_argument("--dry-run", action="store_true", help="report matches, rewrite nothing")
    parser.add_argument("--backup", type=str, default="/tmp/pj_backup", help="backup dir for originals")
    args = parser.parse_args()

    sys.path.insert(0, str(REPO / ".agents" / "skills" / "china-gov-network" / "scripts"))
    import process_tmp
    tmp = REPO / "data" / "tmp"
    targets: list[Path] = []
    for d in sorted(x for x in tmp.iterdir() if x.is_dir()):
        for action in process_tmp.collect_actions(d):
            if not action.valid and action.kind == "unknown":
                targets.append(action.source)

    backup_dir = Path(args.backup)
    stats = {"rewritten": 0, "unmatched": 0, "skipped_nonjson": 0, "families": {}}
    for p in sorted(targets):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            stats["skipped_nonjson"] += 1
            continue
        if not isinstance(doc, dict):
            stats["skipped_nonjson"] += 1
            continue
        out = normalize(doc)
        if _find_nested_unmatched(out):
            stats["unmatched"] += 1
            continue
        out["legacy_raw"] = doc  # zero-loss guarantee: original document always retained
        kind = "person"
        stats["families"][kind] = stats["families"].get(kind, 0) + 1
        if args.dry_run:
            print(f"[dry] {p.relative_to(REPO)}")
            continue
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, backup_dir / f"{p.parent.name}__{p.name}")
        indent = 2
        p.write_text(json.dumps(out, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
        stats["rewritten"] += 1
        print(f"[wrote] {p.relative_to(REPO)}")
    print(f"\nbackup dir: {backup_dir}  stats={stats}")
    return 0


def _find_nested_unmatched(out: dict) -> bool:
    return isinstance(out, dict) and out.get("_unmatched") is True


if __name__ == "__main__":
    raise SystemExit(main())

