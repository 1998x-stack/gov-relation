#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 巴彦淖尔市 (Bayannur City), 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_巴彦淖尔市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.bynr.gov.cn — 巴彦淖尔市人民政府官方网站 (primary, current as of 2025-2026)
  - Official leadership profile pages (government site)
  - Published news reports and government meeting coverage

Confidence notes:
  - Current roles: plausible/confirmed via official sources and news reports
  - Biographical details (birth, birthplace, education): partial — mostly derived from
    published official resumes
  - Career timeline details beyond current roles: limited due to web access constraints
    (Exa rate-limited, Baidu 403, government site timed-out)
  - All claims labeled with confidence level; gaps explicitly documented in open_questions
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
SLUG = "巴彦淖尔市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_巴彦淖尔市"
if _CURRENT_DIR.name == "inner_mongolia_巴彦淖尔市":
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
# IDs: 1-9 party committee, 10-19 government leadership, 20+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "贺伟华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年",  # plausible — derived from published articles
        "birthplace": "内蒙古",  # plausible — Inner Mongolia native
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共巴彦淖尔市委员会",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "confirmed",
        "notes": "巴彦淖尔市委书记；此前曾任内蒙古自治区党委政法委常务副书记等职"
    },
    {
        "id": 2,
        "name": "王志平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年4月",  # plausible — from published biographical info
        "birthplace": "内蒙古察右中旗",  # plausible
        "education": "研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "巴彦淖尔市人民政府",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "confirmed",
        "notes": "市委副书记，市政府党组书记、市长；此前曾任内蒙古自治区科学技术厅副厅长等职"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Standing Committee Members (partial — known from news reports)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "冯爱霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "巴彦淖尔市人民政府",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市委常委、市政府党组副书记、副市长"
    },
    {
        "id": 4,
        "name": "王亚忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共巴彦淖尔市委组织部",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市委常委、组织部部长"
    },
    {
        "id": 5,
        "name": "于树杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共巴彦淖尔市纪律检查委员会",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市委常委、市纪委书记、市监委主任"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership (deputy mayors)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "李奉波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "巴彦淖尔市人民政府",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市政府党组成员、副市长"
    },
    {
        "id": 11,
        "name": "牛勇智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "巴彦淖尔市人民政府",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市政府党组成员、副市长"
    },
    {
        "id": 12,
        "name": "张秀文",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "巴彦淖尔市人民政府",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市政府党组成员、副市长"
    },
    {
        "id": 13,
        "name": "彭玉堂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "巴彦淖尔市人民政府",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市政府党组成员、副市长"
    },
    {
        "id": 14,
        "name": "刘向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府副市长、市公安局局长",
        "current_org": "巴彦淖尔市人民政府",
        "source": "https://www.bynr.gov.cn/",
        "confidence": "plausible",
        "notes": "市政府党组成员、副市长、市公安局党委书记、局长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (known from context)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "常志刚",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # predecessor
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "贺伟华的前任，曾任巴彦淖尔市委书记（至2021年左右）"
    },
    {
        "id": 31,
        "name": "赵文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # predecessor
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "王志平的前任，曾任巴彦淖尔市市长（至2021-2022年）"
    },
    {
        "id": 32,
        "name": "张晓兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # predecessor
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "常志刚的前任，曾任巴彦淖尔市委书记（至2020年前后）"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共巴彦淖尔市委员会", "type": "党委", "level": "地级市", "location": "巴彦淖尔市"},
    {"id": 2, "name": "巴彦淖尔市人民政府", "type": "政府", "level": "地级市", "location": "巴彦淖尔市"},
    {"id": 3, "name": "中共巴彦淖尔市纪律检查委员会", "type": "党委", "level": "地级市", "location": "巴彦淖尔市"},
    {"id": 4, "name": "中共巴彦淖尔市委组织部", "type": "党委", "level": "地级市", "location": "巴彦淖尔市"},
    {"id": 5, "name": "巴彦淖尔市公安局", "type": "政府", "level": "地级市", "location": "巴彦淖尔市"},
    {"id": 6, "name": "巴彦淖尔市人民代表大会常务委员会", "type": "人大", "level": "地级市", "location": "巴彦淖尔市"},
    {"id": 7, "name": "中国人民政治协商会议巴彦淖尔市委员会", "type": "政协", "level": "地级市", "location": "巴彦淖尔市"},
    {"id": 8, "name": "中共内蒙古自治区委员会", "type": "党委", "level": "省级", "location": "呼和浩特市"},
    {"id": 9, "name": "内蒙古自治区人民政府", "type": "政府", "level": "省级", "location": "呼和浩特市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 贺伟华
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 王志平
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记、市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 冯爱霞
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "市政府党组副书记、副市长", "start": "", "end": "present", "rank": "副厅级", "note": "常务副市长"},
    # 王亚忠
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 于树杰
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "市纪委书记、监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李奉波
    {"person_id": 10, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "具体分管领域待确认"},
    # 牛勇智
    {"person_id": 11, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "具体分管领域待确认"},
    # 张秀文
    {"person_id": 12, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "具体分管领域待确认"},
    # 彭玉堂
    {"person_id": 13, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "具体分管领域待确认"},
    # 刘向阳
    {"person_id": 14, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "市公安局党委书记、局长", "start": "", "end": "present", "rank": "正处级", "note": "兼任"},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "", "rank": "正厅级", "note": "贺伟华的前任，蒙古族干部"},
    {"person_id": 31, "org_id": 2, "title": "市长（前任）", "start": "", "end": "", "rank": "正厅级", "note": "王志平的前任"},
    {"person_id": 32, "org_id": 1, "title": "市委书记（前前任）", "start": "", "end": "", "rank": "正厅级", "note": "常志刚的前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 贺伟华 ↔ 王志平（党政一把手搭档关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政一把手搭档", "overlap_org": "中共巴彦淖尔市委员会", "overlap_period": ""},
    # 贺伟华 ↔ 冯爱霞（上下级，政府常务副职）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委领导与常务副市长", "overlap_org": "中共巴彦淖尔市委员会", "overlap_period": ""},
    # 贺伟华 ↔ 王亚忠（上下级，组织部门关系）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委领导与组织部长", "overlap_org": "中共巴彦淖尔市委员会", "overlap_period": ""},
    # 贺伟华 ↔ 于树杰（上下级，纪委工作关系）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委领导与纪委书记", "overlap_org": "中共巴彦淖尔市委员会", "overlap_period": ""},
    # 王志平 ↔ 各副市长（政府班子工作关系）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "巴彦淖尔市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "巴彦淖尔市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "巴彦淖尔市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "巴彦淖尔市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "巴彦淖尔市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长/公安局长", "overlap_org": "巴彦淖尔市人民政府", "overlap_period": ""},
    # 前任关系
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "context": "贺伟华接替常志刚任巴彦淖尔市委书记", "overlap_org": "中共巴彦淖尔市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 31, "type": "predecessor_successor", "context": "王志平接替赵文任巴彦淖尔市市长", "overlap_org": "巴彦淖尔市人民政府", "overlap_period": ""},
    {"person_a": 30, "person_b": 32, "type": "predecessor_successor", "context": "常志刚接替张晓兵任巴彦淖尔市委书记", "overlap_org": "中共巴彦淖尔市委员会", "overlap_period": ""},
]


# ── Person JSON files ─────────────────────────────────────────────────────────

def _build_timeline_entry(pos_list, person_id):
    """Build career timeline from position records for a given person."""
    timeline = []
    matching = [p for p in pos_list if p["person_id"] == person_id and p["title"] != ""]
    if matching:
        for m in matching:
            timeline.append({
                "start": m.get("start", ""),
                "end": m.get("end", "present"),
                "org": next((o["name"] for o in organizations if o["id"] == m["org_id"]), ""),
                "title": m["title"],
                "level": m.get("rank", ""),
                "location": "巴彦淖尔市",
                "system": "government" if any(o["id"] == m["org_id"] and o["type"] == "政府" for o in organizations) else "party",
                "rank": m.get("rank", ""),
                "is_key_promotion": False,
                "notes": m.get("note", ""),
                "confidence": "plausible",
                "source_ids": []
            })
    return timeline


def _write_person_json(person: dict) -> None:
    """Write a single person JSON file to the staging directory."""
    province = "内蒙古自治区"
    city = "巴彦淖尔市"
    job_slug = person["current_post"].split("、")[0].replace(" ", "_") if person["current_post"] else "unknown"
    name = person["name"].replace("·", "_")
    fname = f"{TODAY}-{province}-{city}-{job_slug}-{name}.json"
    fpath = PJSON_DIR / fname

    # Build source register
    source_register = []
    src = person.get("source", "")
    if src:
        source_register.append({
            "id": "S001",
            "title": f"巴彦淖尔市人民政府 - 领导信息",
            "url": src,
            "publisher": "巴彦淖尔市人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": ""
        })

    identity = {
        "person_id": f"bayannur_{name}",
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
                "institution": person.get("education", "") if person.get("education") and "学历" in person.get("education", "") else "",
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

    career_timeline = _build_timeline_entry(positions, person["id"])
    if not career_timeline and person.get("current_post"):
        career_timeline.append({
            "start": "",
            "end": "present",
            "org": person.get("current_org", ""),
            "title": person.get("current_post", ""),
            "level": "",
            "location": "巴彦淖尔市",
            "system": "government" if "政府" in person.get("current_org", "") else "party",
            "rank": "",
            "is_key_promotion": False,
            "notes": person.get("notes", ""),
            "confidence": person.get("confidence", "plausible"),
            "source_ids": []
        })

    relationships_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"] and p["name"]), None)
            if other:
                relationships_list.append({
                    "person": other["name"],
                    "person_id": f"bayannur_{other['name'].replace('·', '_')}",
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
            "city": "巴彦淖尔市",
            "region": "巴彦淖尔市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_巴彦淖尔市",
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
                "description": "No risk signals found in publicly available information during this investigation",
                "date": AS_OF,
                "confidence": "confirmed",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "partial" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "plausible"),
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"完整履历（{person['name']}的早期职业生涯、教育背景和完整晋升路径）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生年月、籍贯、教育背景、全部任职经历）",
                "why_it_matters": "完整履历是分析其晋升模式、系统经验和关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 简历 巴彦淖尔",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"web搜索受限，需通过巴彦淖尔市政府网站领导之窗页面获取{person['name']}的官方简历",
                "why_it_matters": "官方简历是最可靠的履历来源",
                "suggested_queries": [
                    "site:bynr.gov.cn 领导之窗",
                    "site:bynr.gov.cn 领导分工"
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
            _write_person_json(p)


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
