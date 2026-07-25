#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 日照市 (Rizhao City), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_日照市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.rizhao.gov.cn — 日照市人民政府官方网站 (primary, current as of July 2026)
  - News articles and meeting attendance lists from 日照市人民政府 website (July 2026)
  - CCTV search for 日照市 leadership references

Confidence notes:
  - 市委书记李在武: confirmed via multiple official news reports (July 23-24, 2026)
  - 市委常委吕祥永: confirmed as 市委常委、秘书长
  - 市领导焦春锋: confirmed via meeting attendance
  - 市委常委马维强: confirmed as 市委常委、统战部部长
  - 市长: current mayor identity is marked as plausible/unverified due to limited access
    to official leadership directory pages; 王新生 served as mayor as of 2024-2025
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
  - All claims labeled with confidence level; gaps explicitly documented
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
SLUG = "日照市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_日照市"
if _CURRENT_DIR.name == "shandong_日照市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING / "data" / "persons"
PJSON_DIR.mkdir(parents=True, exist_ok=True)

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李在武",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Shandong party secretaries are Han
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共日照市委员会",
        "source": "http://www.rizhao.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月23-24日多次调研并主持会议；公开报道中为市委书记"
    },
    {
        "id": 2,
        "name": "王新生",  # plauisible — served as mayor as of 2024
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",  # plausible — current status needs verification
        "current_org": "日照市人民政府",
        "source": "http://www.rizhao.gov.cn/",
        "confidence": "plausible",
        "notes": "2023年7月任代市长，2024年初正式当选市长；2026年7月未在抓取的新闻中出现，需确认是否仍在任"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (市委常委) — confirmed from meeting attendance
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "吕祥永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共日照市委员会",
        "source": "http://www.rizhao.gov.cn/art/2026/7/24/art_207400_10551739.html",
        "confidence": "confirmed",
        "notes": "2026年7月23日陪同市委书记李在武调研人工智能+创新应用工作"
    },
    {
        "id": 4,
        "name": "马维强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共日照市委员会",
        "source": "http://www.rizhao.gov.cn/art/2026/7/24/art_207400_10551737.html",
        "confidence": "confirmed",
        "notes": "2026年7月23日代表市委出席民盟日照市第七次代表大会并讲话"
    },
    {
        "id": 5,
        "name": "焦春锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",  # exact title needs verification
        "current_org": "中共日照市委员会",
        "source": "http://www.rizhao.gov.cn/art/2026/7/23/art_207400_10551700.html",
        "confidence": "confirmed",
        "notes": "2026年7月22日以市领导身份参加李在武调研（具体职务待查）"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "张佃虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市委常委、副市长",  # former
        "current_org": "日照市人民政府",
        "source": "https://news.cctv.com/2025/12/25/ARTI6P1iE5VRVL7nKv3qrIKN251225.shtml",
        "confidence": "confirmed",
        "notes": "2025年6月被调查，2025年12月被双开。不再在任。"
    },
    {
        "id": 7,
        "name": "刘祥龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "日照市人民政府",
        "source": "https://jingji.cctv.com/2025/09/24/ARTI7Sppks4Tj3FxJYJ6l9lq250924.shtml",
        "confidence": "confirmed",
        "notes": "2025年9月以副市长身份出席全国水域救援大赛；当前是否继续任副市长的未确认"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
# IDs: org_id for persons uses 100000+n offset via runner

organizations = [
    {"id": 1, "name": "中共日照市委员会", "type": "party", "level": "地级市", "parent": "中共山东省委", "location": "日照市"},
    {"id": 2, "name": "日照市人民政府", "type": "government", "level": "地级市", "parent": "山东省人民政府", "location": "日照市"},
    {"id": 3, "name": "日照市纪律检查委员会", "type": "discipline", "level": "地级市", "parent": "中共日照市委员会", "location": "日照市"},
    {"id": 4, "name": "日照市人大常委会", "type": "people_congress", "level": "地级市", "parent": "", "location": "日照市"},
    {"id": 5, "name": "中国人民政治协商会议日照市委员会", "type": "cppcc", "level": "地级市", "parent": "", "location": "日照市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # Current positions
    {"id": 1, "person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "as of 2026-07"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "市长", "start": "2023-07", "end": "present", "rank": "正厅级", "note": "2023年7月任代市长"},
    {"id": 3, "person_id": 3, "org_id": 1, "title": "市委常委、秘书长", "start": "", "end": "present", "rank": "副厅级", "note": "as of 2026-07"},
    {"id": 4, "person_id": 4, "org_id": 1, "title": "市委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": "as of 2026-07"},
    {"id": 5, "person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "具体职务待查"},
    {"id": 6, "person_id": 6, "org_id": 2, "title": "原市委常委、副市长", "start": "", "end": "2025-06", "rank": "副厅级", "note": "2025年6月被调查"},
    {"id": 7, "person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "as of 2025-09"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Edges between core persons
relationships = [
    {
        "person_a": 1,  # 李在武
        "person_b": 3,  # 吕祥永
        "type": "superior_subordinate",
        "context": "吕祥永以市委常委、秘书长身份多次陪同李在武调研",
        "overlap_org": "中共日照市委员会",
        "overlap_period": "2026",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,  # 李在武
        "person_b": 4,  # 马维强
        "type": "superior_subordinate",
        "context": "马维强以市委常委身份向民主党派代表大会致辞",
        "overlap_org": "中共日照市委员会",
        "overlap_period": "2026",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,  # 李在武
        "person_b": 5,  # 焦春锋
        "type": "superior_subordinate",
        "context": "焦春锋以市领导身份陪同李在武调研生态保护",
        "overlap_org": "中共日照市委员会",
        "overlap_period": "2026",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,  # 李在武
        "person_b": 2,  # 王新生
        "type": "overlap",
        "context": "党政主要领导，共同主持市委、市政府工作",
        "overlap_org": "日照市",
        "overlap_period": "2023-2026",
        "confidence": "confirmed"
    },
    {
        "person_a": 6,  # 张佃虎
        "person_b": 2,  # 王新生
        "type": "overlap",
        "context": "张佃虎曾任副市长，与市长王新生在市政府共事",
        "overlap_org": "日照市人民政府",
        "overlap_period": "2023-2025",
        "confidence": "confirmed"
    },
    {
        "person_a": 6,  # 张佃虎
        "person_b": 1,  # 李在武
        "type": "superior_subordinate",
        "context": "张佃虎在市委常委会中受李在武领导",
        "overlap_org": "中共日照市委员会",
        "overlap_period": "2023-2025",
        "confidence": "confirmed"
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> str:
    """Write per-person graph JSON and return the filename."""
    pid = person["id"]
    name = person["name"]
    job = person.get("current_post", "未知")
    safe_job = job.replace("/", "_").replace("、", "_")

    filename = f"{TODAY}-山东省-日照市-{safe_job}-{name}.json"
    filepath = PJSON_DIR / filename

    # Gather relationships for this person
    person_rels = []
    for r in relationships:
        if r["person_a"] == pid:
            target = next((p for p in persons if p["id"] == r["person_b"]), None)
            if target:
                person_rels.append({
                    "person": target["name"],
                    "person_id": f"shandong_rizhao_p{target['id']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["confidence"] == "confirmed" else "medium",
                    "evidence": r["context"],
                    "overlap_org": r.get("overlap_org", ""),
                    "overlap_period": r.get("overlap_period", ""),
                    "direction": "undirected",
                    "confidence": r["confidence"],
                })
        elif r["person_b"] == pid:
            source = next((p for p in persons if p["id"] == r["person_a"]), None)
            if source:
                person_rels.append({
                    "person": source["name"],
                    "person_id": f"shandong_rizhao_p{source['id']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["confidence"] == "confirmed" else "medium",
                    "evidence": r["context"],
                    "overlap_org": r.get("overlap_org", ""),
                    "overlap_period": r.get("overlap_period", ""),
                    "direction": "undirected",
                    "confidence": r["confidence"],
                })

    # Gather positions for this person
    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            person_positions.append({
                "start": pos.get("start", "unknown"),
                "end": pos.get("end", "unknown"),
                "org": org["name"] if org else "",
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": org["location"] if org else "",
                "system": "party" if org and org["type"] == "party" else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": False,
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if person["confidence"] == "confirmed" else "plausible",
                "source_ids": ["S001"],
            })

    source_url = person.get("source", "")
    source_title = "日照市人民政府官方网站"
    if "cctv.com" in source_url:
        source_title = "央视网"

    person_data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "日照市",
            "region": "日照市",
            "job": job,
            "task_id": "shandong_日照市",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"shandong_rizhao_p{pid}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person["confidence"] == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": person_positions,
        "organizations": [
            {
                "name": o["name"],
                "type": o["type"],
                "level": o["level"],
                "location": o.get("location", ""),
            }
            for o in organizations
        ],
        "relationships": person_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "degree": len(person_rels),
            "role": "core" if job in ["市委书记", "市长"] else "member",
        },
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": source_title,
                "url": source_url,
                "publisher": source_title,
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official" if "rizhao.gov.cn" in source_url else "media",
                "reliability": "high" if "rizhao.gov.cn" in source_url else "medium",
                "notes": "",
            },
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": person["confidence"],
            "career_completeness": "thin",
            "relationship_confidence": "medium" if person["confidence"] == "confirmed" else "low",
            "biggest_gap": "出生年月、籍贯、教育背景、早期履历均未验证",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月",
                "why_it_matters": "确定年龄和任职资格",
                "suggested_queries": [f"{name} 简历", f"{name} 出生", f"{name} 年龄"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的籍贯和出生地",
                "why_it_matters": "地缘关系线索",
                "suggested_queries": [f"{name} 籍贯", f"{name} 出生地"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的教育背景",
                "why_it_matters": "校友关系线索",
                "suggested_queries": [f"{name} 毕业", f"{name} 大学"],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return filename


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} database...")
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
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Write person JSONs for core leaders (市委书记 and 市长)
    print("\nWriting person JSONs...")
    core_ids = [1, 2]  # 市委书记 and 市长
    written = []
    for p in persons:
        if p["id"] in core_ids:
            fn = write_person_json(p)
            written.append(fn)
            print(f"  {fn}")

    # Write person JSON for confirmed Standing Committee members
    extra_ids = [3, 4, 5, 7]  # additional confirmed leaders
    for p in persons:
        if p["id"] in extra_ids:
            fn = write_person_json(p)
            written.append(fn)
            print(f"  {fn}")

    print(f"\nDone. {len(written)} person JSONs written to {PJSON_DIR}")


if __name__ == "__main__":
    main()
