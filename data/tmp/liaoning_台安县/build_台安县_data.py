#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 台安县, 鞍山市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_台安县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Web access fully unavailable (all Chinese gov sites, Baidu, Google, Wikipedia blocked)
  - No existing local artifacts for 台安县
  - All data encoded at "unverified" / "plausible" confidence pending web access restoration

Confidence notes:
  - Current officeholders as of 2026-07-25: NAMES UNCONFIRMED due to total web access degradation.
  - The build script, SQLite DB, GEXF graph, and person JSONs are created with placeholder/partial-
    evidence data to satisfy the artifact-generation requirement. All claims are marked unverified.
  - Following leaders were historically associated with 台安县 (pre-2024-2025):
    * 苑振超 (Yuan Zhenchao) — 县委书记, likely rotated in ~2021-2022, status unclear
    * 李克元 (Li Keyuan) — 县长, served as acting/concurrent in ~2022-2023, status unclear
  - Key deputies and full Standing Committee roster unknown.
  - Priority: Re-research when web access is available.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "台安县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_台安县"
if _CURRENT_DIR.name == "liaoning_台安县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=县委书记, 2=县长, 3=县委副书记, 4=常务副县长,
#      5+=副县长/常委

persons = [
    {
        "id": 1,
        "name": "待查（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共台安县委员会",
        "source": "unverified — web access completely unavailable; name TBD",
        "notes": "台安县县委书记。因网络受限（所有政府网站、百度、谷歌均无法访问），姓名暂未确认。"
            "历史上苑振超（Yuan Zhenchao）曾担任该职务至2023-2024年前后。需在网络恢复后查证。",
    },
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "台安县人民政府",
        "source": "unverified — web access completely unavailable; name TBD",
        "notes": "台安县县长。因网络受限，姓名暂未确认。"
            "历史上李克元（Li Keyuan）曾担任该职务至2023-2024年前后。需在网络恢复后查证。",
    },
    {
        "id": 3,
        "name": "待查（县委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共台安县委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县县委副书记。需网络恢复后查证。",
    },
    {
        "id": 4,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "台安县人民政府",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县常务副县长。需网络恢复后查证。",
    },
    {
        "id": 5,
        "name": "待查（县纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共台安县纪律检查委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县纪委书记。需网络恢复后查证。",
    },
    {
        "id": 6,
        "name": "待查（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共台安县委组织部",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县委组织部部长。需网络恢复后查证。",
    },
    {
        "id": 7,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共台安县委政法委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县委政法委书记。需网络恢复后查证。",
    },
    {
        "id": 8,
        "name": "待查（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共台安县委宣传部",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县委宣传部部长。需网络恢复后查证。",
    },
    {
        "id": 9,
        "name": "待查（县委统战部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共台安县委统一战线工作部",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县委统战部部长。需网络恢复后查证。",
    },
    {
        "id": 10,
        "name": "待查（县人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "台安县人大常委会",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县人大主任。需网络恢复后查证。",
    },
    {
        "id": 11,
        "name": "待查（县政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协台安县委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "台安县政协主席。需网络恢复后查证。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共台安县委员会", "type": "党委", "level": "县处级", "parent": "中共鞍山市委员会", "location": "辽宁省鞍山市台安县"},
    {"id": 2, "name": "台安县人民政府", "type": "政府", "level": "县处级", "parent": "鞍山市人民政府", "location": "辽宁省鞍山市台安县"},
    {"id": 3, "name": "台安县人大常委会", "type": "人大", "level": "县处级", "parent": "鞍山市人大常委会", "location": "辽宁省鞍山市台安县"},
    {"id": 4, "name": "政协台安县委员会", "type": "政协", "level": "县处级", "parent": "政协鞍山市委员会", "location": "辽宁省鞍山市台安县"},
    {"id": 5, "name": "中共台安县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共鞍山市纪律检查委员会", "location": "辽宁省鞍山市台安县"},
    {"id": 6, "name": "中共台安县委组织部", "type": "党委", "level": "县处级", "parent": "中共台安县委员会", "location": "辽宁省鞍山市台安县"},
    {"id": 7, "name": "中共台安县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共台安县委员会", "location": "辽宁省鞍山市台安县"},
    {"id": 8, "name": "中共台安县委宣传部", "type": "党委", "level": "县处级", "parent": "中共台安县委员会", "location": "辽宁省鞍山市台安县"},
    {"id": 9, "name": "中共台安县委统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共台安县委员会", "location": "辽宁省鞍山市台安县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "任期待查"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "任期待查"},
    # 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 常务副县长
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 纪委书记
    {"person_id": 5, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 组织部部长
    {"person_id": 6, "org_id": 6, "title": "县委常委、组织部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 政法委书记
    {"person_id": 7, "org_id": 7, "title": "县委常委、政法委书记", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 宣传部部长
    {"person_id": 8, "org_id": 8, "title": "县委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 统战部部长
    {"person_id": 9, "org_id": 9, "title": "县委常委、统战部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 人大主任
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "通常由县委书记兼任或设专职，待查"},
    # 政协主席
    {"person_id": 11, "org_id": 4, "title": "县政协主席", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "任期待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# No confirmed relationships due to complete web access failure.
# Placeholder structure only.

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政领导搭档",
        "context": "县委书记与县长，党政主要负责人关系",
        "overlap_org": "中共台安县委员会/台安县人民政府",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "党委领导班子",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共台安县委员会",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "政府领导班子",
        "context": "县长与常务副县长",
        "overlap_org": "台安县人民政府",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "党委人大关系",
        "context": "县委书记与人大主任（可能兼任）",
        "overlap_org": "中共台安县委员会/台安县人大常委会",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 5, "person_b": 1,
        "type": "监督关系",
        "context": "纪委书记监督党委书记",
        "overlap_org": "中共台安县委员会",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Person JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    """Source register reflecting complete web access failure."""
    return [
        {
            "id": "S001",
            "title": "台安县人民政府官方网站",
            "url": "http://www.taian.ln.gov.cn/",
            "publisher": "台安县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "unreachable",
            "notes": "网站无法访问（DNS解析失败、超时）。多次尝试均失败。",
        },
    ]


def make_person_json(p, relationships_list, source_register):
    """Generate person JSON for a core figure."""
    is_top = p["id"] in (1, 2)
    rank = "县处级正职" if is_top else "县处级副职"
    
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "鞍山市",
            "region": "台安县",
            "job": p["current_post"],
            "task_id": "liaoning_台安县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"taian_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": p["current_org"],
                "title": p["current_post"],
                "level": rank,
                "location": "辽宁省鞍山市台安县",
                "system": "party" if "委" in p["current_org"] and "政府" not in p["current_org"] else "government",
                "rank": rank,
                "is_key_promotion": is_top,
                "notes": "因网络完全受限，当前职务无法确认。需恢复网络后查证。",
                "confidence": "unverified",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [],
        "relationships": [
            {
                "person": rp["name"] if rp["person_a"] != p["id"] else next(
                    (x["name"] for x in persons if x["id"] == rp["person_b"]), ""
                ),
                "person_id": f"taian_{'待查'}",
                "relationship_type": rp["type"],
                "strength": "weak",
                "evidence": rp["context"],
                "overlap_org": rp["overlap_org"],
                "overlap_period": rp["overlap_period"],
                "direction": "undirected",
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
            for rp in relationships_list
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有信息均未确认。因网络访问完全受限（政府网站、百度、谷歌均无法访问），"
                          "县委书记、县长及领导班子全体成员的姓名、履历、关系等全部信息缺失。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"台安县{p['current_post']}的姓名",
                "why_it_matters": "核心领导人的身份信息是整个调查的基础",
                "suggested_queries": [f"台安县 {p['current_post']} 现任", f"台安县 领导之窗"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"台安县{p['current_post']}的完整履历",
                "why_it_matters": "履历是关系网络分析的基础数据",
                "suggested_queries": [f"台安县 {p['current_post']} 简历", f"台安县 {p['current_post']} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "能否通过鞍山市组织部任前公示查到台安县领导班子信息",
                "why_it_matters": "鞍山市网站可能比台安县本级网站更稳定",
                "suggested_queries": ["鞍山市 组织部 任前公示 台安", "鞍山市 人大 任命 台安 县长"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return result


def write_person_jsons():
    """Write per-person JSON files for core leaders."""
    source_register = make_source_register()

    person_relationships = {p["id"]: [] for p in persons}
    for r in relationships:
        if r["person_a"] in person_relationships:
            person_relationships[r["person_a"]].append(r)
        if r["person_b"] in person_relationships and r["person_b"] != r["person_a"]:
            # Create reverse entry
            rev_r = dict(r)
            rev_r["person_a"], rev_r["person_b"] = r["person_b"], r["person_a"]
            person_relationships[r["person_b"]].append(rev_r)

    for p in persons:
        rels = person_relationships.get(p["id"], [])
        pjson = make_person_json(p, rels, source_register)
        filename = f"{TODAY}-辽宁省-鞍山市-{p['current_post'].replace('、', '_').replace('，', '_')}-{p['name']}.json"
        path = PJSON_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full build."""
    print(f"\n{'='*60}")
    print(f"台安县 Network Build (partial-evidence mode)")
    print(f"{'='*60}")
    print(f"Date: {AS_OF}")
    print(f"Web access: UNAVAILABLE — all artifacts in partial-evidence mode")
    print()

    # 1. Database + GEXF
    print("Building database and GEXF...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # 2. Person JSONs
    print("\nWriting person JSONs...")
    write_person_jsons()

    print(f"\n{'='*60}")
    print(f"Build complete.")
    print(f"{'='*60}")
    print(f"DB:      {DB_PATH}")
    print(f"GEXF:    {GEXF_PATH}")
    print(f"Persons: {PJSON_DIR}/")
    print(f"\n⚠️  ALL DATA IS UNVERIFIED — web access was unavailable during research.")
    print(f"   Rebuild when internet access is restored.")
    print()


if __name__ == "__main__":
    main()
