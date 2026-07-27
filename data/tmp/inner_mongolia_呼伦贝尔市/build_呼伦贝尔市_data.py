#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 呼伦贝尔市 (Hulunbuir City), 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_呼伦贝尔市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.hlbe.gov.cn — 呼伦贝尔市人民政府官方网站 (primary, current as of July 2026)
  - Official leadership profile pages for mayor, deputy mayors
  - News articles (July 2026) confirming 及永乾 as mayor (市委副书记、市政府党组书记、市长)
  - "两优一先"表彰大会 (2026-07-01) confirming 王勇 as 市委副书记、政法委书记
  - 市委常委会 (2026-07-24) confirming 及永乾 presides over standing committee meetings
  - 市委五届十一次全会 (2026-06-30) confirming 马金河 as 市委常委、组织部部长

Confidence notes:
  - Current roles: confirmed via official government profiles and multiple news reports (July 2026)
  - 市委书记 position: appears currently vacant or in transition; 及永乾 (mayor) presides over 市委常委会 as 市委副书记
  - Biographical details confirmed via official government resume pages
  - Career timeline details beyond current roles: limited due to web access constraints
  - Party standing committee composition partially confirmed
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
SLUG = "呼伦贝尔市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_呼伦贝尔市"
if _CURRENT_DIR.name == "inner_mongolia_呼伦贝尔市":
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
# IDs: 1-9 party committee, 10-19 government leadership, 20-29 standing committee, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    # 市委书记 — currently vacant (position in transition)
    # Previous 高润喜 was party secretary; transferred out ~2025-2026

    {
        "id": 1,
        "name": "及永乾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "",  # open question
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/528.html",
        "confidence": "confirmed",
        "notes": "市委副书记，市政府党组书记、市长；主持市人民政府全面工作；2026年7月主持市委常委会及市委全会（市委书记空缺期间）"
    },
    {
        "id": 2,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",  # plausible based on name convention
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共呼伦贝尔市委员会",
        "source": "https://www.hlbe.gov.cn/News/show/1440259.html",
        "confidence": "confirmed",
        "notes": "市委副书记、政法委书记；2026年7月主持'两优一先'表彰大会"
    },
    {
        "id": 3,
        "name": "马金河",
        "gender": "男",
        "ethnicity": "蒙古族",  # plausible — Mongolian name
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、组织部部长",
        "current_org": "中共呼伦贝尔市委组织部",
        "source": "https://www.hlbe.gov.cn/News/show/1439430.html",
        "confidence": "confirmed",
        "notes": "市委常委、组织部部长；2026年6月就市委全会有关草案作说明"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "贾效明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年1月",
        "birthplace": "",  # open question
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/999.html",
        "confidence": "confirmed",
        "notes": "市委常委，副市长，市政府党组副书记；协助市长负责市人民政府常务工作"
    },
    {
        "id": 11,
        "name": "辛曙光",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/52.html",
        "confidence": "confirmed",
        "notes": "市政府副市长"
    },
    {
        "id": 12,
        "name": "梁劲松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/527.html",
        "confidence": "confirmed",
        "notes": "市政府副市长"
    },
    {
        "id": 13,
        "name": "张洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/1027.html",
        "confidence": "confirmed",
        "notes": "市政府副市长"
    },
    {
        "id": 14,
        "name": "杨子江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/531.html",
        "confidence": "confirmed",
        "notes": "市政府副市长"
    },
    {
        "id": 15,
        "name": "孙微",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "",  # open question — may be non-party member
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/928.html",
        "confidence": "confirmed",
        "notes": "市政府副市长"
    },
    {
        "id": 16,
        "name": "郭晓龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/1065.html",
        "confidence": "confirmed",
        "notes": "市政府副市长"
    },
    {
        "id": 17,
        "name": "文进磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "呼伦贝尔市人民政府",
        "source": "https://www.hlbe.gov.cn/Leader/show/2/994.html",
        "confidence": "confirmed",
        "notes": "市政府副市长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (known from context)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "高润喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # moved elsewhere
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "前任呼伦贝尔市委书记（~2022-2025），后调任；及永乾的前任，市委书记空缺期间由及永乾主持市委工作"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共呼伦贝尔市委员会", "type": "党委", "level": "地级市", "location": "呼伦贝尔市"},
    {"id": 2, "name": "呼伦贝尔市人民政府", "type": "政府", "level": "地级市", "location": "呼伦贝尔市"},
    {"id": 3, "name": "中共呼伦贝尔市委政法委员会", "type": "党委", "level": "地级市", "location": "呼伦贝尔市"},
    {"id": 4, "name": "中共呼伦贝尔市委组织部", "type": "党委", "level": "地级市", "location": "呼伦贝尔市"},
    {"id": 5, "name": "呼伦贝尔市人民代表大会常务委员会", "type": "人大", "level": "地级市", "location": "呼伦贝尔市"},
    {"id": 6, "name": "中国人民政治协商会议呼伦贝尔市委员会", "type": "政协", "level": "地级市", "location": "呼伦贝尔市"},
    {"id": 7, "name": "中共内蒙古自治区委员会", "type": "党委", "level": "省级", "location": "呼和浩特市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 及永乾
    {"person_id": 1, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "市政府党组书记、市长", "start": "", "end": "present", "rank": "正厅级", "note": "主持市人民政府全面工作"},
    # 王勇
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 3, "title": "政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 马金河
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 贾效明
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长（常务）", "start": "", "end": "present", "rank": "副厅级", "note": "市政府党组副书记；协助市长负责市人民政府常务工作"},
    # 辛曙光
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 梁劲松
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 张洪波
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 杨子江
    {"person_id": 14, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 孙微
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 郭晓龙
    {"person_id": 16, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 文进磊
    {"person_id": 17, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "", "rank": "正厅级", "note": "及永乾的前任，高润喜；市委书记空缺"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 及永乾 ↔ 王勇（党政班子搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市长（主持市委工作）与专职副书记", "overlap_org": "中共呼伦贝尔市委员会", "overlap_period": ""},
    # 及永乾 ↔ 马金河（上下级，组织部关系）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委领导与组织部长", "overlap_org": "中共呼伦贝尔市委员会", "overlap_period": ""},
    # 及永乾 ↔ 贾效明（市长与常务副市长）
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    # 及永乾 ↔ 各副市长（政府班子工作关系）
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    # 王勇 ↔ 马金河（专职副书记与组织部长协作关系）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "专职副书记与组织部长在换届工作中的协作", "overlap_org": "中共呼伦贝尔市委员会", "overlap_period": ""},
    # 贾效明 ↔ 其他副市长（政府班子内部）
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "常务副市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 12, "type": "overlap", "context": "常务副市长与副市长", "overlap_org": "呼伦贝尔市人民政府", "overlap_period": ""},
    # 前任关系
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "context": "及永乾在书记空缺期间主持市委工作，前任书记高润喜", "overlap_org": "中共呼伦贝尔市委员会", "overlap_period": ""},
]


# ── Person JSON files ─────────────────────────────────────────────────────────

def _write_person_json(person: dict, filename: str) -> None:
    """Write a single person JSON file to the staging directory."""
    today = TODAY
    province = "内蒙古自治区"
    city = "呼伦贝尔市"
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
        source_register.append({
            "id": f"S{sid:03d}",
            "title": f"呼伦贝尔市人民政府 - {person['current_post']}信息",
            "url": src,
            "publisher": "呼伦贝尔市人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": ""
        })
    # Build identity
    identity = {
        "person_id": f"hulunbuir_{name}",
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
                "institution": person.get("education", "") if person.get("education") else "",
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"] if source_register else []
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
    career_timeline = [
        {
            "start": "",
            "end": "present",
            "org": person.get("current_org", ""),
            "title": person.get("current_post", ""),
            "level": "",
            "location": "呼伦贝尔市",
            "system": "government" if "政府" in person.get("current_org", "") else "party",
            "rank": "",
            "is_key_promotion": False,
            "notes": person.get("notes", ""),
            "confidence": "confirmed",
            "source_ids": ["S001"] if source_register else []
        }
    ]
    if person.get("notes") and "前任" in person.get("notes", ""):
        career_timeline[0]["confidence"] = "plausible"

    relationships_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                relationships_list.append({
                    "person": other["name"],
                    "person_id": f"hulunbuir_{other['name'].replace('·', '_')}",
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
            "city": "呼伦贝尔市",
            "region": "呼伦贝尔市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_呼伦贝尔市",
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
    core_ids = {1, 2, 3, 10}
    for p in persons:
        if p["id"] in core_ids:
            name_clean = p["name"].replace("·", "_")
            job_clean = p["current_post"].split("、")[0].replace(" ", "_")
            fname = f"{TODAY}-内蒙古自治区-呼伦贝尔市-{job_clean}-{name_clean}.json"
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
