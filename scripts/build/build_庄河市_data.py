#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 庄河市, 大连市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_庄河市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - Web access fully unavailable (all Chinese gov sites, Baidu, Google, Wikipedia blocked)
  - No existing local artifacts
  - All data encoded at "unverified" / "plausible" confidence pending web access restoration

Confidence notes:
  - Current officeholders as of 2026-07-25: NAMES UNCONFIRMED due to total web access degradation.
  - The build script, SQLite DB, GEXF graph, and person JSONs are created with placeholder/partial-
    evidence data to satisfy the artifact-generation requirement. All claims are marked unverified.
  - Following leaders were historically associated with 庄河市 (pre-2024):
    * 申守勃 (Shen Shoubo) — 市委书记, likely rotated out by 2025-2026
    * 孙功利 (Sun Gongli) — 市长, likely rotated out by 2025-2026
  - Key deputies and full Standing Committee roster unknown.
  - Prior attempts (worker-2, worker-4) also failed due to network conditions.
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
SLUG = "庄河市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_庄河市"
if _CURRENT_DIR.name == "liaoning_庄河市":
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
# IDs: 1=市委书记, 2=市长, 3=市委副书记, 4=常务副市长,
#      5+=副市长/常委

persons = [
    {
        "id": 1,
        "name": "待查（市委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共庄河市委员会",
        "source": "unverified — web access completely unavailable; name TBD",
        "notes": "庄河市市委书记。因网络受限（所有政府网站、百度、谷歌均无法访问），姓名暂未确认。"
            "历史上申守勃曾担任该职务至2024年前后。需在网络恢复后查证。",
    },
    {
        "id": 2,
        "name": "待查（市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "庄河市人民政府",
        "source": "unverified — web access completely unavailable; name TBD",
        "notes": "庄河市市长。因网络受限，姓名暂未确认。"
            "历史上孙功利曾担任该职务至2024年前后。需在网络恢复后查证。",
    },
    {
        "id": 3,
        "name": "待查（市委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共庄河市委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市市委副书记。需网络恢复后查证。",
    },
    {
        "id": 4,
        "name": "待查（常务副市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "庄河市人民政府",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市常务副市长。需网络恢复后查证。",
    },
    {
        "id": 5,
        "name": "待查（市纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共庄河市纪律检查委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市纪委书记。需网络恢复后查证。",
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
        "current_post": "市委常委、组织部部长",
        "current_org": "中共庄河市委组织部",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市委组织部部长。需网络恢复后查证。",
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
        "current_post": "市委常委、政法委书记",
        "current_org": "中共庄河市委政法委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市委政法委书记。需网络恢复后查证。",
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
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共庄河市委宣传部",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市委宣传部部长。需网络恢复后查证。",
    },
    {
        "id": 9,
        "name": "待查（市委统战部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共庄河市委统一战线工作部",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市委统战部部长。需网络恢复后查证。",
    },
    {
        "id": 10,
        "name": "待查（市人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "庄河市人大常委会",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市人大主任。需网络恢复后查证。",
    },
    {
        "id": 11,
        "name": "待查（市政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协庄河市委员会",
        "source": "unverified — web access completely unavailable",
        "notes": "庄河市政协主席。需网络恢复后查证。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共庄河市委员会", "type": "党委", "level": "县处级", "parent": "中共大连市委员会", "location": "辽宁省大连市庄河市"},
    {"id": 2, "name": "庄河市人民政府", "type": "政府", "level": "县处级", "parent": "大连市人民政府", "location": "辽宁省大连市庄河市"},
    {"id": 3, "name": "庄河市人大常委会", "type": "人大", "level": "县处级", "parent": "大连市人大常委会", "location": "辽宁省大连市庄河市"},
    {"id": 4, "name": "政协庄河市委员会", "type": "政协", "level": "县处级", "parent": "政协大连市委员会", "location": "辽宁省大连市庄河市"},
    {"id": 5, "name": "中共庄河市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共大连市纪律检查委员会", "location": "辽宁省大连市庄河市"},
    {"id": 6, "name": "中共庄河市委组织部", "type": "党委", "level": "县处级", "parent": "中共庄河市委员会", "location": "辽宁省大连市庄河市"},
    {"id": 7, "name": "中共庄河市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共庄河市委员会", "location": "辽宁省大连市庄河市"},
    {"id": 8, "name": "中共庄河市委宣传部", "type": "党委", "level": "县处级", "parent": "中共庄河市委员会", "location": "辽宁省大连市庄河市"},
    {"id": 9, "name": "中共庄河市委统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共庄河市委员会", "location": "辽宁省大连市庄河市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "任期待查"},
    # 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "任期待查"},
    # 市委副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 常务副市长
    {"person_id": 4, "org_id": 2, "title": "市委常委、常务副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 纪委书记
    {"person_id": 5, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 组织部部长
    {"person_id": 6, "org_id": 6, "title": "市委常委、组织部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 政法委书记
    {"person_id": 7, "org_id": 7, "title": "市委常委、政法委书记", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 宣传部部长
    {"person_id": 8, "org_id": 8, "title": "市委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 统战部部长
    {"person_id": 9, "org_id": 9, "title": "市委常委、统战部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "任期待查"},
    # 人大主任
    {"person_id": 10, "org_id": 3, "title": "市人大常委会主任", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "通常由市委书记兼任或设专职，待查"},
    # 政协主席
    {"person_id": 11, "org_id": 4, "title": "市政协主席", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "任期待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# No confirmed relationships due to complete web access failure.
# Placeholder structure only.

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政领导搭档",
        "context": "市委书记与市长，党政主要负责人关系",
        "overlap_org": "中共庄河市委员会/庄河市人民政府",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "党委领导班子",
        "context": "市委书记与市委副书记",
        "overlap_org": "中共庄河市委员会",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "政府领导班子",
        "context": "市长与常务副市长",
        "overlap_org": "庄河市人民政府",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "党委人大关系",
        "context": "市委书记与人大主任（可能兼任）",
        "overlap_org": "中共庄河市委员会/庄河市人大常委会",
        "overlap_period": "任期待查",
        "confidence": "unverified",
    },
    {
        "person_a": 5, "person_b": 1,
        "type": "监督关系",
        "context": "纪委书记监督党委书记",
        "overlap_org": "中共庄河市委员会",
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
            "title": "庄河市人民政府官方网站",
            "url": "https://www.zhuanghe.gov.cn/",
            "publisher": "庄河市人民政府",
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
            "city": "大连市",
            "region": "庄河市",
            "job": p["current_post"],
            "task_id": "liaoning_庄河市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"zhuanghe_{p['name']}",
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
                "location": "辽宁省大连市庄河市",
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
                "person_id": f"zhuanghe_{'待查'}",
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
                          "市委书记、市长及领导班子全体成员的姓名、履历、关系等全部信息缺失。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"庄河市{p['current_post']}的姓名",
                "why_it_matters": "核心领导人的身份信息是整个调查的基础",
                "suggested_queries": [f"庄河市 {p['current_post']} 现任", f"庄河市 领导之窗"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"庄河市{p['current_post']}的完整履历",
                "why_it_matters": "履历是关系网络分析的基础数据",
                "suggested_queries": [f"庄河市 {p['current_post']} 简历", f"庄河市 {p['current_post']} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "能否通过大连市组织部任前公示查到庄河市领导班子信息",
                "why_it_matters": "大连市网站可能比庄河市本级网站更稳定",
                "suggested_queries": ["大连市 组织部 任前公示 庄河", "大连市 人大 任命 庄河 市长"],
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
        filename = f"{TODAY}-辽宁省-大连市-{p['current_post'].replace('、', '_').replace('，', '_')}-{p['name']}.json"
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
    print(f"庄河市 Network Build (partial-evidence mode)")
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
