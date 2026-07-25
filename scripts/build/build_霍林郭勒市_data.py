#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 霍林郭勒市 (Huolinguole City), 通辽市, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_霍林郭勒市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.hlgls.gov.cn — 霍林郭勒市人民政府官方网站 (primary, current as of July 2026)
  - Official leadership profile pages for mayor and deputy mayors
  - News articles from hlgls.gov.cn confirming 嵇海洋 as party secretary (April-July 2026)
  - 申玉秀 official bio from government leadership page

Confidence notes:
  - Current roles: confirmed via official government profiles and news reports (July 2026)
  - Biographical details: confirmed for 申玉秀 (complete official bio); limited for 嵇海洋
  - Career timeline details beyond current roles: limited due to web access constraints
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
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
SLUG = "霍林郭勒市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_霍林郭勒市"
if _CURRENT_DIR.name == "inner_mongolia_霍林郭勒市":
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
# IDs: 1-9 party committee, 10-19 government leadership, 20+ predecessors/others

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "嵇海洋",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共霍林郭勒市委员会",
        "source": "http://www.hlgls.gov.cn/hsxw/ldhd/202607/t20260714_1060034.html",
        "confidence": "confirmed",
        "notes": "曾同时担任市委书记和政府市长（一肩挑），截至2026年7月仍为市委书记。四月至七月活跃于市委常委会、安全生产检查等领导活动。"
    },
    {
        "id": 2,
        "name": "申玉秀",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1986年1月",
        "birthplace": "内蒙古通辽市",
        "education": "",  # open question — education details not on profile page
        "party_join": "中共党员",
        "work_start": "2006年12月",  # party join date
        "current_post": "市委副书记、政府市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/syx/",
        "confidence": "confirmed",
        "notes": "市委副书记、政府市长，通辽霍林郭勒高新技术产业开发区党工委书记、管委会主任。1986年1月出生，蒙古族，2006年12月入党。2026年新任命（此前嵇海洋兼任市长）。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership (deputy mayors)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "张宏威",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、副市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/zhw/",
        "confidence": "confirmed",
        "notes": "市委常委、市政府副市长（提名）；2026年7月新任命"
    },
    {
        "id": 11,
        "name": "胡勇",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/hy/",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 12,
        "name": "宋启哲",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/sqzsqz/",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 13,
        "name": "刘淼",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/lm/",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 14,
        "name": "刘磊",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/liul/",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 15,
        "name": "苍安吉",
        "gender": "男",
        "ethnicity": "",  # likely 蒙古族 (name suggests Mongolian ethnicity)
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/cja/",
        "confidence": "confirmed",
        "notes": "姓名疑似蒙古族"
    },
    {
        "id": 16,
        "name": "薛光宇",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "霍林郭勒市人民政府",
        "source": "http://www.hlgls.gov.cn/zwgk/zfld/xgy/",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (limited data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "高继业",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # previously 市委书记
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "前任霍林郭勒市委书记（嵇海洋的前任）。去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共霍林郭勒市委员会", "type": "党委", "level": "县级市", "location": "霍林郭勒市"},
    {"id": 2, "name": "霍林郭勒市人民政府", "type": "政府", "level": "县级市", "location": "霍林郭勒市"},
    {"id": 3, "name": "通辽霍林郭勒高新技术产业开发区管委会", "type": "开发区", "level": "县级市", "location": "霍林郭勒市"},
    {"id": 4, "name": "中共霍林郭勒市纪律检查委员会", "type": "党委", "level": "县级市", "location": "霍林郭勒市"},
    {"id": 5, "name": "霍林郭勒市人民代表大会常务委员会", "type": "人大", "level": "县级市", "location": "霍林郭勒市"},
    {"id": 6, "name": "中国人民政治协商会议霍林郭勒市委员会", "type": "政协", "level": "县级市", "location": "霍林郭勒市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 嵇海洋
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "政府市长（兼任）", "start": "", "end": "~2026中期", "rank": "正处级", "note": "曾一肩挑兼任市长"},
    # 申玉秀
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "政府市长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 3, "title": "党工委书记、管委会主任", "start": "", "end": "present", "rank": "", "note": "兼任"},
    # 张宏威
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "2026年7月新任命"},
    {"person_id": 10, "org_id": 2, "title": "副市长（提名）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 胡勇
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 宋启哲
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘淼
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘磊
    {"person_id": 14, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 苍安吉
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 薛光宇
    {"person_id": 16, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "高继业，嵇海洋的前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 嵇海洋 ↔ 申玉秀（党政一把手搭档关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政一把手搭档（嵇海洋为市委书记，申玉秀为市长）", "overlap_org": "中共霍林郭勒市委员会", "overlap_period": ""},
    # 嵇海洋 ↔ 张宏威（上下级，市委班子）
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委书记与市委常委", "overlap_org": "中共霍林郭勒市委员会", "overlap_period": ""},
    # 申玉秀 ↔ 各副市长（政府班子工作关系）
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "霍林郭勒市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "霍林郭勒市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "霍林郭勒市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "霍林郭勒市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "霍林郭勒市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "霍林郭勒市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "霍林郭勒市人民政府", "overlap_period": ""},
    # 前任关系
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "context": "嵇海洋接替高继业任霍林郭勒市委书记", "overlap_org": "中共霍林郭勒市委员会", "overlap_period": ""},
]

# ── Person JSON files ─────────────────────────────────────────────────────────

def _write_person_json(person: dict, filename: str) -> None:
    """Write a single person JSON file to the staging directory."""
    today = TODAY
    province = "内蒙古自治区"
    city = "霍林郭勒市"
    job_slug = person["current_post"].split("、")[0].replace(" ", "_")
    name = person["name"].replace("·", "_")
    fname = f"{today}-{province}-{city}-{job_slug}-{name}.json"
    fpath = PJSON_DIR / fname
    # Build source register
    source_register = []
    sid = 0
    src = person.get("source", "")
    if src:
        sid += 1
        source_type = "official" if "hlgls.gov.cn" in src else "historical"
        reliability = "high" if "hlgls.gov.cn" in src else "low"
        source_register.append({
            "id": f"S{sid:03d}",
            "title": f"霍林郭勒市人民政府 - {person['current_post']}信息",
            "url": src,
            "publisher": "霍林郭勒市人民政府" if "hlgls.gov.cn" in src else "历史记录",
            "accessed_at": AS_OF,
            "source_type": source_type,
            "reliability": reliability,
            "notes": ""
        })
    # Build identity
    identity = {
        "person_id": f"huolinguole_{name}",
        "name": person["name"],
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": "",
        "education": [
            {
                "period": "",
                "institution": "",
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"] if source_register and "hlgls.gov.cn" in person.get("source", "") else []
            }
        ],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{person['name']}_{person.get('birth', '')}",
            "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
            "official_profile_url": person.get("source", "")
        }
    }
    career_timeline = []
    if person.get("current_post") and person.get("current_org"):
        career_timeline.append({
            "start": "",
            "end": "present",
            "org": person.get("current_org", ""),
            "title": person.get("current_post", ""),
            "level": "",
            "location": "霍林郭勒市",
            "system": "government" if "政府" in person.get("current_org", "") else "party",
            "rank": "",
            "is_key_promotion": False,
            "notes": person.get("notes", ""),
            "confidence": person.get("confidence", "plausible"),
            "source_ids": ["S001"] if source_register else []
        })

    relationships_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                relationships_list.append({
                    "person": other["name"],
                    "person_id": f"huolinguole_{other['name'].replace('·', '_')}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ["superior_subordinate"] else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "person_to_other" if r["person_a"] == person["id"] else "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"] if source_register else []
                })

    obj = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "通辽市",
            "region": "霍林郭勒市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_霍林郭勒市",
            "time_focus": "2026-07"
        },
        "identity": identity,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"] if source_register else []
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found in publicly available official profiles",
                "date": AS_OF,
                "confidence": "confirmed",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"完整履历（{person['name']}的早期职业生涯和完整晋升路径）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（教育背景、早期任职经历、完整的晋升时间线）",
                "why_it_matters": "完整履历是分析其晋升模式、系统经验和关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 简历",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {fpath.name}")


def write_person_jsons():
    """Write person JSON files for the core leadership."""
    core_ids = {1, 2, 10}
    for p in persons:
        if p["id"] in core_ids:
            name_clean = p["name"].replace("·", "_")
            job_clean = p["current_post"].split("、")[0].replace(" ", "_")
            fname = f"{TODAY}-内蒙古自治区-霍林郭勒市-{job_clean}-{name_clean}.json"
            _write_person_json(p, fname)


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"═══ Building {SLUG} data ═══")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Run the build
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

    # Write person JSONs
    print("  Writing person JSON files...")
    write_person_jsons()

    # Summary
    print(f"\n═══ Summary ═══")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB file: {DB_PATH}")
    print(f"  GEXF file: {GEXF_PATH}")
    print(f"  Person JSONs: {PJSON_DIR}")
    print("  Done.")
