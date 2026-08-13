#!/usr/bin/env python3
"""Reusable: emit schema-1.0 person graph JSON from a build_<region>_data.py.

Parses the `persons`/`organizations`/`relationships` python-literal lists in a
build script and writes a person JSON for each requested {name:job} into a
staging dir. Filippo Writes directly to staging; promote with
scripts/process_tmp.py after review.

Usage:
  python3 scripts/tools/gen_person_json.py \
      --build scripts/build/build_兴安盟_data.py \
      --province 内蒙古自治区 --parent_city 兴安盟 --region 兴安盟 \
      --task inner_mongolia_兴安盟 \
      --jobs "奇飞云:盟委书记,于吉顺:盟长" \
      --stage data/tmp/inner_mongolia_兴安盟
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def load_build_data(path: str) -> dict:
    src = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(src)
    out = {"persons": [], "organizations": [], "relationships": [], "positions": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                name = getattr(target, "id", "")
                if name in out and isinstance(node.value, ast.List):
                    out[name] = ast.literal_eval(node.value)
    return out


def org_for_id(orgs: list[dict], oid) -> str:
    for o in orgs:
        if str(o.get("id")) == str(oid):
            return o.get("name", "")
    return ""


def _name_for_id(persons: list[dict], pid) -> str:
    for p in persons:
        if str(p.get("id")) == str(pid):
            return p.get("name", str(pid))
    return str(pid)


def _mk_person_doc(p: dict, persons: list[dict], orgs: list[dict], rels: list[dict],
                   positions: list[dict], meta: dict) -> dict:
    pid = str(p.get("id"))
    rels_out = []
    for r in rels:
        a, b = str(r.get("person_a")), str(r.get("person_b"))
        if a == pid:
            other, direction = b, "person_to_other"
        elif b == pid:
            other, direction = a, "other_to_person"
        else:
            continue
        rels_out.append({
            "person": _name_for_id(persons, other),
            "person_id": "",
            "relationship_type": r.get("type", "overlap"),
            "strength": "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": direction,
            "confidence": "plausible",
            "source_ids": [],
        })

    # career timeline from positions rows (schema-1.0)
    timeline = []
    for pos in positions:
        if str(pos.get("person_id")) != pid:
            continue
        timeline.append({
            "start": pos.get("start_date", "unknown"),
            "end": pos.get("end_date", "present"),
            "org": org_for_id(orgs, pos.get("org_id")),
            "title": pos.get("title", ""),
            "level": "",
            "location": "",
            "system": "other",
            "rank": pos.get("rank", ""),
            "is_key_promotion": False,
            "notes": pos.get("note", ""),
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })
    if not timeline:
        timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口",
            "title": "", "notes": "公开资料未找到完整履历",
            "confidence": "unverified", "source_ids": [],
        })

    birth = p.get("birth", "待查")
    nl = []
    for x in [p.get("department_info"), p.get("education"), p.get("academic")]:
        if x:
            nl.append({"period": "", "institution": str(x), "major": "",
                       "degree": "", "study_type": "unknown", "source_ids": []})

    return {
        "schema_version": "1.0",
        "generated_at": meta["date"],
        "investigation_scope": {
            "province": meta["province"], "city": meta["parent_city"],
            "region": meta["region"], "job": meta["job"],
            "task_id": meta["task_id"], "time_focus": "当前在任调研",
        },
        "identity": {
            "person_id": f'{meta["slug"]}_{p.get("name", "")}',
            "name": p.get("name", ""), "aliases": [],
            "gender": p.get("gender", "待查"),
            "ethnicity": p.get("ethnicity", "待查"),
            "birth": birth, "birthplace": p.get("birthplace", "待查"),
            "native_place": "待查", "education": nl,
            "party_join": p.get("party_join", "待查"),
            "work_start": p.get("work_start", "待查"),
            "dedupe_keys": {
                "name_birth": f"{p.get('name','')}_{birth}",
                "name_birthplace": f"{p.get('name','')}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "", "as_of": meta["date"],
            "is_current_confirmed": True, "source_ids": ["S001"],
        },
        "career_timeline": timeline,
        "organizations": [{"name": p.get("current_org", ""), "role": p.get("current_post", ""),
                           "from": "", "to": "present"}],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": [],
            "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格依据公开记录推断。",
        },
        "risk_and_integrity_signals": [],
        "source_register": [{
            "id": "S001", "title": p.get("source", ""), "url": p.get("source", ""),
            "publisher": "", "published_at": "", "accessed_at": meta["date"],
            "source_type": "official", "reliability": "high", "notes": "",
        }],
        "confidence_summary": {
            "identity": "partial", "current_role": "confirmed",
            "career_completeness": "partial", "relationship_confidence": "low",
            "biggest_gap": "出生/学历/履历细节未公开",
        },
        "open_questions": [],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--province", required=True)
    ap.add_argument("--parent_city", required=True)
    ap.add_argument("--region", required=True)
    ap.add_argument("--task", required=True)
    ap.add_argument("--jobs", required=True, help="commas: 名:职务")
    ap.add_argument("--stage", required=True)
    a = ap.parse_args()

    data = load_build_data(a.build)
    orgs = data["organizations"]
    job_map = {}
    for tok in a.jobs.split(","):
        if ":" in tok:
            n, j = tok.split(":", 1)
            job_map[n.strip()] = j.strip()

    meta = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "province": a.province, "parent_city": a.parent_city, "region": a.region,
        "task_id": a.task, "slug": a.region,
    }
    os.makedirs(a.stage, exist_ok=True)
    seen = 0
    for p in data["persons"]:
        name = p.get("name", "")
        if name not in job_map:
            continue
        meta["job"] = job_map[name]
        doc = _mk_person_doc(p, data["persons"], orgs, data["relationships"],
                              data["positions"], meta)
        fname = f"{meta['date']}-{a.province}-{a.parent_city}-{meta['job']}-{name}.json"
        (Path(a.stage) / fname).write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        seen += 1
        print("  ", fname)
    print(f"wrote {seen} person JSON -> {a.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())